from classes.app import App


def main():
    msg = "Input window dimensions in the form 'width, height':\n If left \
           empty, will default to 600x185"
    try:
        dimensions = input(msg)
        if dimensions == "":
            width = 600
            height = 185
        else:
            width = int(dimensions.split(", ")[0])
            height = int(dimensions.split(", ")[1])
    except(IndexError, ValueError):
        print("Error with input. Using default values...")
        width = 600
        height = 185
    finally:
        app = App(width, height)
        app.start()


if __name__ == "__main__":
    main()
