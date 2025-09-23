import os, shutil
folder = input("Drop the folder path here, to do magic :)  ")
file = ["Images", "Docs", "Videos", "Music"]
exts = [[".jpg", ".png",".jpeg"], [".pdf", ".docx"], [".mp4"], [".mp3"]]
for a in os.listdir(folder):
    name, ext = os.path.splitext(a)
    if os.path.isdir(os.path.join(folder, a)):
        continue

    for i in range(len(file)):
        if ext in exts[i]:
            dest = os.path.join(folder, file[i])
            if not os.path.exists(dest):
                os.makedirs(dest)
            shutil.move(os.path.join(folder, a), os.path.join(dest, a))
            print(f"This {a} is moved to {file[i]} <3 ")
            break
    else:
        print(f"{a} Must be a different extension file :o")

print("\n There you go the folder is sorted:3")

   

                              
