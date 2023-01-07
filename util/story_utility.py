import os
import pickle
from datetime import datetime

from data_models import StoryContent, CombinedWorkdir


class StoryUtility:

    @staticmethod
    def save_story(workdir: str, story_content: StoryContent) -> str:
        """
        Save the given story into a pickle file
        :param workdir: directory where to save the story
        :param story_content: contents of the story
        """
        filepath = os.path.join(workdir, f"story_content.pickle")
        with open(filepath, "wb") as file:
            pickle.dump(story_content, file)
        return filepath

    @staticmethod
    def load_story_from_pickle(pickle_file: str) -> StoryContent:
        """
        Load the given story from pickle file
        :param pickle_file: a pickle file for a previously generated story
        :return: The story content
        """
        print("Loading existing story")
        with open(pickle_file, "rb") as file:
            return pickle.load(file)

    @staticmethod
    def new_workdir(prompt: str) -> CombinedWorkdir:
        workdir = StoryUtility._generate_new_workdir_name(prompt)
        workdir_images = f"{workdir}/images"
        workdir_pages = f"{workdir}/pages"
        workdir_audio = f"{workdir}/audio"

        if not os.path.isdir(workdir):
            os.mkdir(workdir)
        if not os.path.isdir(workdir_images):
            os.mkdir(workdir_images)
        if not os.path.isdir(workdir_pages):
            os.mkdir(workdir_pages)
        if not os.path.isdir(workdir_audio):
            os.mkdir(workdir_audio)

        return CombinedWorkdir(
            workdir=workdir,
            workdir_images=workdir_images,
            workdir_pages=workdir_pages,
            workdir_audio=workdir_audio
        )

    @staticmethod
    def _generate_new_workdir_name(story_prompt: str) -> str:
        now = datetime.now()
        month = str(now.month).zfill(2)
        day = str(now.day).zfill(2)
        hour = str(now.hour).zfill(2)
        minute = str(now.minute).zfill(2)
        second = str(now.second).zfill(2)
        return f"_stories/{now.year}_{month}_{day}_{hour}_{minute}_{second}-{'_'.join(story_prompt.split(' '))}"
