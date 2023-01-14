from typing import Optional, Tuple

from data_models import StoryContent, CombinedWorkdir, StorySize
from generators.story_content_generator import StoryContentGenerator
from util.story_utility import StoryUtility


class StoryProvider:
    """
    Provide the contents of the story (image and text).
    """

    def __init__(
        self,
        story_utility: StoryUtility,
        story_content_generator: StoryContentGenerator,
    ):
        self.story_utility = story_utility
        self.story_content_generator = story_content_generator

    def generate_or_load(
        self,
        story_prompt: Optional[str],
        pickle_file: Optional[str],
        story_size: StorySize,
    ) -> Tuple[CombinedWorkdir, StoryContent]:
        """Generate a new story or load existing story from pickle file."""

        if story_prompt is None and pickle_file is None:
            raise RuntimeError("You have to provide either a prompt or a pickle file.")

        if story_prompt and pickle_file:
            raise RuntimeError(
                "You have to provide either a prompt or a pickle file, not both."
            )

        if pickle_file:
            assert pickle_file is not None
            # If a pickle file is provided, read it then create a new workdir based on the observed story seed.
            # This enables continuation without recalling expensive text/image generation APIs.
            # And it also avoids overriding previous work, always create a new workdir.
            story_content = self.story_utility.load_story_from_pickle(
                pickle_file=pickle_file
            )
            combined_workdir: CombinedWorkdir = self.story_utility.new_workdir(
                story_content.story_seed
            )
        else:
            assert story_prompt is not None
            # If a pickle file is not provided, create a new workdir first based on the given story prompt.
            # Then, generate a new story.
            combined_workdir = self.story_utility.new_workdir(story_prompt)
            story_content = self.story_content_generator.generate_new_story(
                workdir_images=combined_workdir.workdir_images,
                story_seed_prompt=story_prompt,
                story_size=story_size,
            )

        # Save the story content anyway. If it's new, save it for later access/continuation.
        # If it's loaded from pickle, re-save it to the new workdir for easy debugging.
        self.story_utility.save_story(
            workdir=combined_workdir.workdir, story_content=story_content
        )

        return combined_workdir, story_content
