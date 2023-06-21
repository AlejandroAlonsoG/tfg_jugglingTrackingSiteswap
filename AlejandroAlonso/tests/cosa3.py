from PIL import Image
from matplotlib import pyplot as plt

def show_images_side_by_side(image_paths, labels):
    images = [Image.open(path) for path in image_paths]
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    
    for i, image in enumerate(images):
        axes[i].imshow(image)
        axes[i].axis('off')
        axes[i].set_title(labels[i])  # Agregar título a la imagen
    
    plt.show()

# Rutas de las imágenes que deseas abrir y mostrar
image_paths = ['/home/alex/Pictures/cap1.png', '/home/alex/Pictures/cap2.png', '/home/alex/Pictures/cap3.png']

# Etiquetas para cada imagen
labels = ['Siteswap 3', 'Siteswap 71', 'Siteswap 645']

# Llamada a la función para mostrar las imágenes
show_images_side_by_side(image_paths, labels)
