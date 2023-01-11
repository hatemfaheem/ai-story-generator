# AI Story Generator

Generate stories using AI. From text to story (pdf and video).

Example videos can be found here: https://www.youtube.com/@ai-story

A sample story can be found under _stories dir. The sample contains raw content (image, text and audio) alongside `final_video.mp4` and `final_story.pdf`

Generate stories using AI. From text to story (pdf and video).

## High Level Diagram

![Alt text](docs/high-level-diagram.png?raw=true "Title")

## Prerequisuites

Install `requirements.txt`.

## Try it with a pre-generated story

```
python3 main.py --help
```

Process a pre-generated story.

```
python3 main.py --pickle ./_stories/2023_01_06_17_38_47-Five_Little_Monkeys/story_content.pickle
```

## Generate a new Story

### Open AI Credentials

1. Register with open AI beta: https://beta.openai.com/
2. Get organization and api key.
3. Create a local file named `openai_creds.json` with the below format and put it root dir of the project.

```
{
  "organization":  "xxx-XXXXXXXX",
  "api_key":  "xx-XXXXXXXXXXXXXXXXXXXXXXXXX"
}
```

### Pass a prompt instead of a pickle file

Replace "The Friendly Panda" with your favorite story title/prompt.

```
python3 main.py --prompt "The Friendly Panda"
```

## Check Results

Results can be found under _stories directory with a new dir prefixed with date and time of run.

## Important Note

Open AI has limitations/restrictions on what kind of content you can create. So, it may fail to generate text or images for specific words and sentences. 

https://openai.com/dall-e-2/
