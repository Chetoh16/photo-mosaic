from photomosaic import *

if __name__ == "__main__":

    # image chosen to be mosaic-ed
    input_image_path = "assets/alex-ege-pics/SS853599.JPG"

    # directory of source images (should be squares)
    source_images_dir_path = "assets/square-source-pics"

    # size of each square tile block in pixels
    tile_size = 30
    
    # load and scale input images
    source_images = load_and_scale_source_images(source_images_dir_path, tile_size)


    # manage cache
    cache = JSONCache("./mean_rgb_cache.json")
    if not cache.has_data():
        print("Cachne not found; calculating. Cashing in.")
        source_rgbs = get_avg_rgb_for_images(source_images)
        cache.write_all(source_rgbs)
    else:
        print("Cache found; loading. Cha Ching.")
        source_rgbs = cache.read_all()


    print("Building the mosaic one beautiful image at a time.")
    mosaic_image = build_photomosaic_image(input_image_path, source_images, source_rgbs, tile_size)


    # get filename and add '_mosaic.jpg'
    base_name = os.path.splitext(os.path.basename(input_image_path))[0]
    output_name = f"{base_name}_mosaic.jpg"
    
    # save output image
    mosaic_image.save(output_name)

    print(f"Success! Saved as: {output_name}")

    mosaic_image.show()
