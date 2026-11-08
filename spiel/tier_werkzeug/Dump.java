import jassimp.*;
import java.util.*;
import java.io.*;
import java.lang.reflect.*;
import org.lwjgl.util.vector.*;
import zombie.core.skinnedmodel.model.jassimp.*;
import zombie.core.skinnedmodel.animation.*;

/** Schreibt je Clip und Abtastzeit die Modellraum-Matrizen aller Knochen als Text; dazu Haut-Daten. Nur lesen, startet das Spiel nicht.
 *  Aufruf: Dump <datei> <ausgabe.txt> [skin]   (skin: auch Punkte, Gewichte, Knochenindizes, Offsetmatrizen) */
public class Dump {
  static Object f(Object o, String n) throws Exception { Field x=o.getClass().getDeclaredField(n); x.setAccessible(true); return x.get(o); }
  static Keyframe lerpAt(Keyframe[] k, float t){ return null; }
  public static void main(String[] a) throws Exception {
    String path=a[0];
    EnumSet<AiPostProcessSteps> st=EnumSet.of(AiPostProcessSteps.FIND_INSTANCES,AiPostProcessSteps.MAKE_LEFT_HANDED,AiPostProcessSteps.LIMIT_BONE_WEIGHTS,AiPostProcessSteps.TRIANGULATE,AiPostProcessSteps.OPTIMIZE_MESHES,AiPostProcessSteps.REMOVE_REDUNDANT_MATERIALS,AiPostProcessSteps.JOIN_IDENTICAL_VERTICES);
    Jassimp.setLibraryLoader(new JassimpLibraryLoader(){ @Override public void loadLibrary(){ System.loadLibrary("jassimp64"); } });
    AiScene sc=Jassimp.importFile(path,st);
    ProcessedAiSceneParams p=ProcessedAiSceneParams.create();
    p.scene=sc; p.mode=JAssImpImporter.LoadMode.Normal; p.skinnedTo=null; p.meshName=null;
    p.animBonesScaleModifier=1f; p.animBonesRotateModifier=null;
    ProcessedAiScene ps=ProcessedAiScene.process(p);
    Object sk=f(ps,"skeleton");
    HashMap<String,Integer> bi=(HashMap<String,Integer>)f(sk,"boneIndices");
    ArrayList<Integer> hier=(ArrayList<Integer>)f(sk,"skeletonHierarchy");
    ArrayList<Matrix4f> off=(ArrayList<Matrix4f>)f(sk,"skinOffsetMatrices");
    ArrayList<Matrix4f> bind=(ArrayList<Matrix4f>)f(sk,"bindPose");
    HashMap<String,AnimationClip> clips=(HashMap<String,AnimationClip>)f(sk,"clips");
    String[] names=new String[bi.size()]; for(Map.Entry<String,Integer> e: bi.entrySet()) names[e.getValue()]=e.getKey();
    PrintWriter w=new PrintWriter(new BufferedWriter(new FileWriter(a[1])));
    w.println("BONES "+names.length);
    for(int i=0;i<names.length;i++) w.println(names[i]+" "+hier.get(i));
    w.println("OFFSET");
    for(int i=0;i<names.length;i++) wm(w,off.get(i));
    w.println("BIND");
    for(int i=0;i<names.length;i++) wm(w,bind.get(i));
    for (Map.Entry<String,AnimationClip> e: clips.entrySet()) {
      AnimationClip c=e.getValue();
      ArrayList<ArrayList<Keyframe>> per=new ArrayList<>();
      for(int i=0;i<names.length;i++) per.add(new ArrayList<>());
      for(Keyframe k: c.getKeyframes()) if(k.bone>=0) per.get(k.bone).add(k);
      TreeSet<Float> times=new TreeSet<>();
      for(ArrayList<Keyframe> l: per) for(Keyframe k:l) times.add(k.time);
      w.println("CLIP "+e.getKey()+" "+c.getDuration()+" "+times.size());
      StringBuilder nk=new StringBuilder("NOKEYS");
      for(int i=0;i<names.length;i++) if(per.get(i).isEmpty()) nk.append(' ').append(names[i]);
      w.println(nk);
      for(float t: times){
        w.println("T "+t);
        Matrix4f[] model=new Matrix4f[names.length];
        for(int i=0;i<names.length;i++){
          Keyframe best=null,nxt=null;
          for(Keyframe k: per.get(i)){ if(k.time<=t+1e-5f) best=k; if(k.time>=t-1e-5f && nxt==null) nxt=k; }
          Matrix4f loc=new Matrix4f();
          if(best==null) best=nxt;
          if(best!=null) zombie.core.skinnedmodel.HelperFunctions.CreateFromQuaternionPositionScale(best.position,best.rotation,best.scale,loc);
          model[i]=new Matrix4f();
          int par=hier.get(i);
          if(par<0) model[i].load(loc); else Matrix4f.mul(loc,model[par],model[i]);
          if(best!=null) w.println("L "+i+" "+best.position.x+" "+best.position.y+" "+best.position.z+" "+best.rotation.x+" "+best.rotation.y+" "+best.rotation.z+" "+best.rotation.w+" "+best.scale.x+" "+best.scale.y+" "+best.scale.z);
          wm(w,model[i]);
        }
      }
    }
    if(a.length>2){
      Object sm=f(ps,"skinnedMesh");
      zombie.core.skinnedmodel.model.VertexBufferObject.VertexArray va=(zombie.core.skinnedmodel.model.VertexBufferObject.VertexArray)f(sm,"vertices");
      int[] el=(int[])f(sm,"elements");
      w.println("ELEMENTS "+el.length);
      StringBuilder sb=new StringBuilder(); for(int v: el) sb.append(v).append(' '); w.println(sb);
      w.println("VERTS "+va.numVertices);
      for(int v=0;v<va.numVertices;v++){
        w.println(va.getElementFloat(v,0,0)+" "+va.getElementFloat(v,0,1)+" "+va.getElementFloat(v,0,2)+" "
          +va.getElementFloat(v,2,0)+" "+va.getElementFloat(v,2,1)+" "+va.getElementFloat(v,2,2)+" "+va.getElementFloat(v,2,3)+" "
          +(int)va.getElementFloat(v,3,0)+" "+(int)va.getElementFloat(v,3,1)+" "+(int)va.getElementFloat(v,3,2)+" "+(int)va.getElementFloat(v,3,3)+" "
          +va.getElementFloat(v,4,0)+" "+va.getElementFloat(v,4,1)+" "+va.getElementFloat(v,1,0)+" "+va.getElementFloat(v,1,1)+" "+va.getElementFloat(v,1,2));
      }
    }
    w.close();
    System.out.println("OK "+path+" Knochen "+names.length+" Clips "+clips.keySet());
  }
  static void wm(PrintWriter w, Matrix4f m){
    w.println(m.m00+" "+m.m01+" "+m.m02+" "+m.m03+" "+m.m10+" "+m.m11+" "+m.m12+" "+m.m13+" "+m.m20+" "+m.m21+" "+m.m22+" "+m.m23+" "+m.m30+" "+m.m31+" "+m.m32+" "+m.m33);
  }
}
