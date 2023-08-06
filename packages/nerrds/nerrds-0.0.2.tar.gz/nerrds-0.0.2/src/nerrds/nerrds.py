

from importlib import resources

def main():
	print('this bit works')
	with resources.path("nerrds.scripts.AMBER", "leap.in") as f:  # use this for the package
		data_file_path = f

	print(f)



if __name__ == "__main__":
    main()
