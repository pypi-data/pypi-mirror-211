import os
import shutil
import argparse

marked_files = []

'''
The "subsys config" command should be available for the user to configure the repo.

The "subsys config" must be structured this way “subsys config --code [QUIZ_CODE] --student_id [STUDENT_ID]”.
'''

def config(args):
    if(args.code != None and args.student_id!= None):
        print("Configuration details:")
        print(f"Quiz code: {args.code}")
        print(f"Student ID: {args.student_id}")

        # Ask for approval
        while True:
            approval = input("Do you approve the configuration? (yes/no): ").lower()
            if approval == "yes":
                print("Configuration approved.")
                break
            elif approval == "no":
                print("Configuration not approved.")
                break
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")

    else:
        print("The 'subsys config' must be structured this way : 'subsys config --code [QUIZ_CODE] --student_id [STUDENT_ID]'.")

'''
initialize a directory as an assignment submission using the “subsys init” command.
now init function which initializes a directory as an assignment submission.
'''

def init():
    current_directory = os.getcwd()
    project_name = os.path.basename(current_directory)
    assignment_directory = os.path.join(current_directory, "submission")

    if os.path.exists(assignment_directory):
        print("Error: Submission directory already exists.")
        return

    try:
        os.mkdir(assignment_directory)
        print(f"Submission directory created: {assignment_directory}")

        # Additional initialization steps if needed

    except Exception as e:
        print(f"Error creating submission directory: {e}")
        

def mark_files(file_paths):
    global marked_files
    marked_files.extend(file_paths)
    print("Files marked for capture.")

def push_files(server_url):
    global marked_files
    if not marked_files:
        print("No files marked for capture.")
        return

    try:
        for file_path in marked_files:
            file_name = os.path.basename(file_path)
            destination = os.path.join(server_url, file_name)
            shutil.copy(file_path, destination)

        print(f"Files pushed to server at: {server_url}")
    except Exception as e:
        print(f"Error pushing files to server: {e}")
    finally:
        marked_files = []  # Clear the marked files list after pushing

def move_to_directory(directory_path):
    os.chdir(directory_path)
    print(f"Moved to directory: {os.getcwd()}")
