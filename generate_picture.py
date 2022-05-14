from PIL import Image
import datetime
import numpy

IS_LEAP_YEAR = datetime.datetime.now().year%4 == 0
IN_PATH = "profile.png"
OUT_PATH = "rotated_profile.png"

if IS_LEAP_YEAR:
    DAYS_IN_MONTH = [31,28,31,30,31,30,31,31,30,31,30,31]
else:
    DAYS_IN_MONTH = [31,29,31,30,31,30,31,31,30,31,30,31]

def get_rotation_amount() -> float:
    """
        Returns the amount to rotate the profile picture
        such that it performs a full rotation once per year
        :return: Number of degrees to rotate today's profile picture by
    """
    now = datetime.datetime.now()
    day = now.day
    month = now.month - 1  # -1 to turn [1,12] -> [0,11]. 0 indexed month number

    # If January, this will be range(0,-1), which is empty.
    # Otherwise, this will just be the list of month #s that we have completed this year
    months_to_sum = range(0, month-1)
    day_of_year = sum([DAYS_IN_MONTH[x] for x in months_to_sum]) + day

    if IS_LEAP_YEAR:
        return (day_of_year / 366) * 360
    return (day_of_year / 365) * 360

def generate_rotated_image(deg:float) -> None:
    """
        Rotates the image at IN_PATH, and saves it at OUTPATH
        :param deg: Degrees to rotate image by
        :return: None. Generates file at OUT_PATH
    """

    with Image.open(IN_PATH) as image:
        rotated_image = image.rotate(deg)
        
        # Rotating image will introduce some black pixels. Need to make those white like the
        # background.
        rotated_image.convert('RGBA')
        data = numpy.array(rotated_image)
        data[data == (0,0,0)] = 255
        result_image = Image.fromarray(data)
        result_image.save(OUT_PATH)

def generate_todays_pic():
    generate_rotated_image(get_rotation_amount())


if __name__ == "__main__":
    generate_todays_pic()
    angle = get_rotation_amount()
    print(f"Today's theta: {angle} ")
