import email
from pathlib import Path

# file = Path("Delete notifications for ht_text_pd dataset[220].eml")
# file = Path("Delete notifications for ht_text_pd_open_access dataset[41].eml")
file = Path("Delete notifications for ht_text_pd_world dataset[180].eml")
# file = Path("Delete notifications for ht_text_pd_world_open_access dataset[49].eml")

text_data = ''

with open(file, 'r') as f:
    msg = email.message_from_file(f)
    # print(msg)
    if msg.is_multipart():
        print('multi')
    else:
        payload = msg.get_payload(decode=True)
        strtext = payload.decode()
        dt = msg.get('date')
        # print(dt)
        # print(strtext)
        print('single')
        text_data = strtext

usefull_data = text_data.split('===')[2].split()
# print(text_data)
for data in usefull_data:
    temp_data = data.split('.')
    dir_name = temp_data[0]
    vol_name = temp_data[1]
    #   print(dir_name+"->"+vol_name)

dir_name = 'loc'
vol_name = 'ark+=13960=t8ff3w38m'
path = Path('data_sets/sample-pairtree-data-set-2')

my_path = path / dir_name


def rm_tree(pth):
    pth = Path(pth)
    for child in pth.glob('*'):
        if child.is_file():
            child.unlink()
        else:
            rm_tree(child)
    pth.rmdir()


if my_path.exists():
    dir_root = my_path / 'pairtree_root'
    vol_names = [vol_name[i:i + 2] for i in range(0, len(vol_name), 2)]
    for i in range(0, len(vol_names)):
        dir_root = dir_root / vol_names[i]
    if dir_root.exists():
        print(dir_root)
        s = list(dir_root.glob('*' + vol_name + "*"))
        print(s)
        if s:
            for item in s:
                if item.is_dir():
                    rm_tree(item)
                else:
                    item.unlink()
                print('Deleted :' +  vol_name + " @ " + item)
        else:
            print("Already deleted/ nothing inside")

    else:
        print('No pairtree folder or files for ' + vol_name)
else:
    print('No dir of ' + my_path)
