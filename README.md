# Minecraft Mod Texture Upscaler

Most mods ship with custom textures that are the default 16x textures that Minecraft uses. When playing with a resource pack 
such as Faithful 32x, these custom textures can look out of place.

This simple tool will extract all textures from a mod's jar file and upscale them using the Scale2x algorithm. They will be output
to a directory that can be zipped and used as a resource pack in game. The upscaled textures will override the default 16x textures
in the mod's jar file.

## Dependencies

- [Scale2x](https://github.com/amadvance/scale2x)
    - `scalerx` must be installed and in your PATH
    - If on Windows you can extract it to `./scale2x`

## Usage

1. Create an output directory
2. Create an `.mcmetadata` file in the output directory with the following:

```json
"pack": {
    "pack_format": 15,
    "description": "32x custom resource pack"
}
```

3. Run the `main.py` script (scale factor is 2 by default):

```bat
python main.py <input jar> <output dir> [scale factor]
```

e.g.

```bat
python main.py ../supplementaries-1.20-2.8.17.jar ../my_custom_pack-32x-1.20.1 2
```

4. Zip the `assets` directory and `pack.mcmeta` in the output directory and that's the resource pack ready to be used in game!

