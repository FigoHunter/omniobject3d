import os
import tarfile

data_path='./OpenXD-OmniObject3D-New'

for root, dirs, files in os.walk(data_path):
    for file in files:
        file = os.path.join(root, file)
        if file.endswith('.tar.gz'):
            target = file.removesuffix('.tar.gz')
            try:
                print('extracting: '+file)
                tar = tarfile.open(file,':gz')
                for extracted_file in tar.getnames():
                    if not os.path.exists(os.path.join(target, extracted_file)):
                        tar.extract(extracted_file,target)
                    else:
                        print('skip: '+extracted_file)
                tar.close()
            except Exception as e:
                print(e)
                print("Fail with: " + str(file))