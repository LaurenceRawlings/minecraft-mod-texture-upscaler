import os
import shutil
import subprocess
import sys
import tempfile
import zipfile


def progressbar(it, prefix="", size=60, out=sys.stdout):
    count = len(it)

    def show(j):
        x = int(size * j / count)
        print(
            "{}[{}{}] {}/{}".format(prefix, "#" * x, "." * (size - x), j, count),
            end="\r",
            file=out,
            flush=True,
        )

    show(0)
    for i, item in enumerate(it):
        yield item
        show(i + 1)
    print("", flush=True, file=out)


def upscale_exe(input, output, scale=2):
    subprocess.run(["scalerx", "-k", str(scale), input, output])


if __name__ == "__main__":
    if len(os.sys.argv) < 3:
        print("Usage: python main.py <input jar> <output dir> [upscale factor]")
        exit(1)

    input_jar = os.sys.argv[1]
    output_dir = os.sys.argv[2]
    scale = 2

    if os.path.exists("./scale2x/scalerx.exe"):
        os.environ["PATH"] = os.pathsep.join(
            [os.path.abspath("./scale2x"), os.environ["PATH"]]
        )
    if not shutil.which("scalerx"):
        print(
            "scalerx not found! Install it from https://github.com/amadvance/scale2x/releases"
        )
        exit(1)

    if not os.path.exists(input_jar):
        print("Input jar does not exist!")
        exit(1)

    if not os.path.exists(output_dir):
        print("Output directory does not exist!")
        exit(1)

    if len(os.sys.argv) > 3:
        try:
            scale = int(os.sys.argv[3])
        except ValueError:
            print("Upscale factor must be an integer!")
            exit(1)

    with zipfile.ZipFile(input_jar, "r") as zip_ref:
        print(f"Searching {input_jar} for textures")
        textures = [
            file.filename
            for file in zip_ref.infolist()
            if file.filename.startswith("assets/")
            and "/textures/" in file.filename
            and file.filename.endswith(".png")
        ]

        if len(textures) == 0:
            print("No textures found.")
            exit(0)

        texture_count = len(textures)
        print(f"Found {texture_count} texture{'' if texture_count == 1 else 's'}")

        with tempfile.TemporaryDirectory() as tmp_dir:
            print(f"Extracting textures to temporary directory {tmp_dir}")
            for filename in progressbar(textures):
                zip_ref.extract(filename, tmp_dir)

            print(f"Upscaling textures and saving to {output_dir}")
            for filename in progressbar(textures):
                imput_file = os.path.join(tmp_dir, filename)
                output_file = os.path.join(output_dir, filename)
                os.makedirs(os.path.dirname(output_file), exist_ok=True)

                upscale_exe(imput_file, output_file, scale)

            print("Cleaning up temporary directory")

    print("Done!")
    exit(0)
