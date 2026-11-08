import jassimp.*;
import java.util.*;
import java.lang.reflect.*;
import org.lwjgl.util.vector.*;
import zombie.core.skinnedmodel.model.jassimp.*;
import zombie.core.skinnedmodel.animation.*;

public class Probe {
  static Object f(Object o, String n) throws Exception { Field x=o.getClass().getDeclaredField(n); x.setAccessible(true); return x.get(o); }
  static void tree(AiNode n, int d) {
    StringBuilder s=new StringBuilder(); for(int i=0;i<d;i++) s.append("  ");
    System.out.println(s+n.getName()+(n.getNumMeshes()>0?" [mesh]":""));
    for (Object c: n.getChildren()) tree((AiNode)c,d+1);
  }
  public static void main(String[] a) throws Exception {
    String path=a[0]; String kind=a[1];
    EnumSet<AiPostProcessSteps> st=EnumSet.of(AiPostProcessSteps.FIND_INSTANCES,AiPostProcessSteps.MAKE_LEFT_HANDED,AiPostProcessSteps.LIMIT_BONE_WEIGHTS,AiPostProcessSteps.TRIANGULATE,AiPostProcessSteps.OPTIMIZE_MESHES,AiPostProcessSteps.REMOVE_REDUNDANT_MATERIALS,AiPostProcessSteps.JOIN_IDENTICAL_VERTICES);
    Jassimp.setLibraryLoader(new JassimpLibraryLoader(){ @Override public void loadLibrary(){ System.loadLibrary("jassimp64"); } });
    AiScene sc=Jassimp.importFile(path,st);
    AiBuiltInWrapperProvider w=new AiBuiltInWrapperProvider();
    AiNode root=(AiNode)sc.getSceneRoot(w);
    System.out.println("== "+path);
    System.out.println("root="+root.getName()+" meshes="+sc.getNumMeshes()+" anims="+sc.getNumAnimations());
    if (a.length>2) tree(root,0);
    for (AiMesh m: sc.getMeshes()) {
      float[] mn={1e9f,1e9f,1e9f},mx={-1e9f,-1e9f,-1e9f};
      for(int i=0;i<m.getNumVertices();i++){float[] v={m.getPositionX(i),m.getPositionY(i),m.getPositionZ(i)};for(int k=0;k<3;k++){mn[k]=Math.min(mn[k],v[k]);mx[k]=Math.max(mx[k],v[k]);}}
      System.out.println("mesh "+m.getName()+" v="+m.getNumVertices()+" bones="+m.getBones().size()+" bbox "+Arrays.toString(mn)+" "+Arrays.toString(mx)+" uv="+m.hasTexCoords(0)+(m.hasTexCoords(0)?" UVPROBE u="+m.getTexCoordU(0,0)+" v="+m.getTexCoordV(0,0):""));
    }
    for (AiAnimation an: sc.getAnimations()) {
      int pos=0,rot=0,scl=0; for(AiNodeAnim c: an.getChannels()){pos+=c.getNumPosKeys();rot+=c.getNumRotKeys();scl+=c.getNumScaleKeys();}
      System.out.println("anim '"+an.getName()+"' dur="+an.getDuration()+" tps="+an.getTicksPerSecond()+" ch="+an.getChannels().size()+" keys p/r/s "+pos+"/"+rot+"/"+scl);
    }
    // Weg wie im Lader
    ProcessedAiSceneParams p=ProcessedAiSceneParams.create();
    p.scene=sc; p.mode=JAssImpImporter.LoadMode.Normal; p.skinnedTo=null; p.meshName=null;
    if(kind.equals("fbx")){ Quaternion q=new Quaternion(); q.setFromAxisAngle(new Vector4f(1,0,0,(float)(-Math.PI/2))); p.animBonesScaleModifier=0.01f; p.animBonesRotateModifier=q; }
    else { p.animBonesScaleModifier=1f; p.animBonesRotateModifier=null; }
    ProcessedAiScene ps=ProcessedAiScene.process(p);
    Object sk=f(ps,"skeleton");
    if(sk==null){System.out.println("KEIN SKELETT (statisch behandelt)");return;}
    HashMap<String,Integer> bi=(HashMap<String,Integer>)f(sk,"boneIndices");
    ArrayList<Integer> hier=(ArrayList<Integer>)f(sk,"skeletonHierarchy");
    ArrayList<Matrix4f> off=(ArrayList<Matrix4f>)f(sk,"skinOffsetMatrices");
    HashMap<String,AnimationClip> clips=(HashMap<String,AnimationClip>)f(sk,"clips");
    String[] names=new String[bi.size()]; for(Map.Entry<String,Integer> e: bi.entrySet()) names[e.getValue()]=e.getKey();
    System.out.println("bones "+bi.size()+" hierarchy "+hier);
    System.out.println("names "+Arrays.toString(names));
    System.out.println("clips "+clips.keySet());
    for (Map.Entry<String,AnimationClip> e: clips.entrySet()) {
      AnimationClip c=e.getValue();
      Keyframe[] kf=c.getKeyframes();
      Matrix4f[] model=new Matrix4f[names.length];
      boolean[] have=new boolean[names.length];
      Keyframe[] first=new Keyframe[names.length]; Keyframe[] last=new Keyframe[names.length];
      for(Keyframe k: kf){ if(k.bone<0)continue; if(first[k.bone]==null)first[k.bone]=k; last[k.bone]=k; have[k.bone]=true; }
      StringBuilder nok=new StringBuilder();
      for(int i=0;i<names.length;i++){ if(first[i]==null) nok.append(names[i]).append(' '); }
      System.out.println("clip "+e.getKey()+" dauer="+c.getDuration()+" frames="+kf.length+" ohne_keys: "+nok);
      for(int i=0;i<names.length;i++){
        Matrix4f loc=new Matrix4f();
        if(first[i]!=null) zombie.core.skinnedmodel.HelperFunctions.CreateFromQuaternionPositionScale(first[i].position,first[i].rotation,first[i].scale,loc);
        model[i]=new Matrix4f();
        int par=hier.get(i);
        if(par<0) model[i].load(loc); else Matrix4f.mul(loc,model[par],model[i]);
      }
      for(String n: new String[]{"Dummy01","Bip01","Bip01_Pelvis","Bip01_Head","Bip01_L_Foot","Bip01_Tail","Translation_Data"}){
        Integer i=bi.get(n); if(i==null)continue;
        System.out.printf(Locale.ROOT,"  %s idx=%d welt=(%.3f %.3f %.3f)%n",n,i,model[i].m03,model[i].m13,model[i].m23);
      }
      Integer b1=bi.get("Bip01"); if(b1!=null&&first[b1]!=null) System.out.printf(Locale.ROOT,"  Bip01 LOKAL pos=(%.3f %.3f %.3f) keys bis t=%.3f%n",first[b1].position.x,first[b1].position.y,first[b1].position.z,last[b1].time);
      Integer td=bi.get("Translation_Data");
      if(td!=null&&first[td]!=null){ Vector3f l=last[td].position; System.out.printf(Locale.ROOT,"  Translation_Data Ende pos=(%.4f %.4f %.4f) -> deferred (x,-z)=(%.4f,%.4f) t=%.3f%n",l.x,l.y,l.z,l.x,-l.z,last[td].time); }
      // Skinning-Probe: Netz in Ruhehaltung durch die erste Pose schicken
      Object sm=f(ps,"skinnedMesh");
      if(sm!=null){
        zombie.core.skinnedmodel.model.VertexBufferObject.VertexArray va=(zombie.core.skinnedmodel.model.VertexBufferObject.VertexArray)f(sm,"vertices");
        float[] mn={1e9f,1e9f,1e9f},mx={-1e9f,-1e9f,-1e9f};
        for(int v=0;v<va.numVertices;v++){
          float x=va.getElementFloat(v,0,0),y=va.getElementFloat(v,0,1),z=va.getElementFloat(v,0,2);
          float rx=0,ry=0,rz=0;
          for(int k=0;k<4;k++){
            float wt=va.getElementFloat(v,2,k); int b=(int)va.getElementFloat(v,3,k); if(wt<=0)continue;
            Matrix4f sk2=new Matrix4f(); Matrix4f.mul(off.get(b),model[b],sk2);
            // Schreibweise der Engine: m03/m13/m23 sind die Verschiebung, also Zeile/Spalte
            float px=sk2.m00*x+sk2.m01*y+sk2.m02*z+sk2.m03;
            float py=sk2.m10*x+sk2.m11*y+sk2.m12*z+sk2.m13;
            float pz=sk2.m20*x+sk2.m21*y+sk2.m22*z+sk2.m23;
            rx+=wt*px;ry+=wt*py;rz+=wt*pz;
          }
          mn[0]=Math.min(mn[0],rx);mn[1]=Math.min(mn[1],ry);mn[2]=Math.min(mn[2],rz);mx[0]=Math.max(mx[0],rx);mx[1]=Math.max(mx[1],ry);mx[2]=Math.max(mx[2],rz);
        }
        System.out.printf(Locale.ROOT,"  gehaeutet bbox (%.3f %.3f %.3f)..(%.3f %.3f %.3f)%n",mn[0],mn[1],mn[2],mx[0],mx[1],mx[2]);
      }
    }
  }
}
