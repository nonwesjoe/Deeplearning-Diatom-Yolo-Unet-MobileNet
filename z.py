import torch
from torchvision import transforms
from PIL import Image
print('-----------z-ready--------------')
# classes={0: 'Achnanthidium', 1: 'Adlafia', 2: 'Amphora', 3: 'Caloneis', 4: 'Cocconeis', 5: 'Cymbella', 6: 'Cymbopleura', 7: 'Denticula', 8: 'Diatoma', 9: 'Didymosphenia', 10: 'Diploneis', 11: 'Encyonema', 12: 'Epithemia', 13: 'Fragilaria', 14: 'Frustulia', 15: 'Gomphonema', 16: 'Halamphora', 17: 'Hantzschiana', 18: 'Humidophila', 19: 'Luticola', 20: 'Meridion', 21: 'Navicula', 22: 'Neidiomorpha', 23: 'Nitzschia', 24: 'Pantocsekiella', 25: 'Pinnularia', 26: 'Planothidium', 27: 'Rhoicosphenia', 28: 'Sellaphora', 29: 'Stauroneis', 30: 'Surella', 31: 'Surirella'}
classes={0: 'Achnanthidium biasolettianum', 1: 'Achnanthidium minutissimum', 2: 'Adlafia minuscula', 3: 'Amphora inariensis', 4: 'Amphora pediculus', 5: 'Caloneis lancettula', 6: 'Cocconeis pseudolineata', 7: 'Cymbella cantonatii', 8: 'Cymbella excisa', 9: 'Cymbella excisa var. procera', 10: 'Cymbella excisa var. subcapitata', 11: 'Cymbopleura amphicephala', 12: 'Denticula kuetzingii', 13: 'Diatoma mesodon', 14: 'Diatoma moniliformis', 15: 'Didymosphenia geminata', 16: 'Diploneis fontanella', 17: 'Encyonema silesiacum', 18: 'Encyonema ventricosum', 19: 'Epithemia argus', 20: 'Epithemia goeppertiana', 21: 'Fragilaria recapitellata', 22: 'Frustulia vulgaris', 23: 'Gomphonema calcifugum', 24: 'Gomphonema drutelingense', 25: 'Gomphonema exilissimum', 26: 'Gomphonema micropus', 27: 'Gomphonema minutum', 28: 'Gomphonema olivaceum', 29: 'Gomphonema pumilum', 30: 'Gomphonema pumilum var. rigidum', 31: 'Gomphonema supertergestinum', 32: 'Gomphonema tergestinum', 33: 'Halamphora paraveneta', 34: 'Halamphora veneta', 35: 'Hantzschiana abundans', 36: 'Humidophila contenta', 37: 'Humidophila perpusilla', 38: 'Luticola nivalis', 39: 'Meridion circulare', 40: 'Navicula capitatoradiata', 41: 'Navicula cryptocephala', 42: 'Navicula cryptotenella', 43: 'Navicula cryptotenelloides', 44: 'Navicula gregaria', 45: 'Navicula lanceolata', 46: 'Navicula moskalii', 47: 'Navicula novaesiberica', 48: 'Navicula reichardtiana', 49: 'Navicula tripunctata', 50: 'Navicula trivialis', 51: 'Navicula upsaliensis', 52: 'Neidiomorpha binodiformis', 53: 'Nitzschia archibaldii', 54: 'Nitzschia hantzschiana', 55: 'Nitzschia linearis', 56: 'Nitzschia palea', 57: 'Nitzschia recta', 58: 'Pantocsekiella ocellata', 59: 'Pinnularia brebissonii', 60: 'Planothidium frequentissimum', 61: 'Planothidium lanceolatum', 62: 'Rhoicosphenia abbreviata', 63: 'Sellaphora radiosa', 64: 'Sellaphora saugerresii', 65: 'Stauroneis blazenciciae', 66: 'Surella minuta', 67: 'Surirella brebissonii var. kuetzingii'}

model = torch.load('dex.pth', map_location=torch.device('cpu'))

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])


def model_output(model,image_path):  # input model and img path | output class name
    # 加载模型
    image = Image.open(image_path).convert('RGB')  # 将图片转换为RGB格式
    input_tensor = transform(image)
    input_batch = input_tensor.unsqueeze(0)

    with torch.no_grad():
        output = model(input_batch)
        _, predicted = torch.max(output, 1)
    name = classes[predicted.item()]
    return name

# cla=model_output(model,'wsz/s/0.png')

