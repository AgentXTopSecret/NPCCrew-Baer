import sys,os
from PIL import Image
A=sys.argv[1]; out=sys.argv[2]; names=sys.argv[3].split(","); cols=int(sys.argv[4]) if len(sys.argv)>4 else 4
ims=[Image.open(os.path.join(A,n+".png")).convert("RGB") for n in names]
w,h=ims[0].size; rows=(len(ims)+cols-1)//cols
s=Image.new("RGB",(cols*w,rows*h))
for i,im in enumerate(ims): s.paste(im,((i%cols)*w,(i//cols)*h))
s.save(out); print(out,s.size)
