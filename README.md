# Story AI

StoryAI 프로젝트는 인공지능을 활용하여 소설을 자동으로 생성하는 프로젝트입니다.
캐릭터를 생성하며 캐릭터들 각각의 시놉시스를 생성할 수 있습니다.

## 요구 사항
- Python 3.11 이상

## 설치 방법
```
pip install https://github.com/paust-team/storyai/releases/download/v0.1.0/storyai-0.1.0-py3-none-any.whl
```

## 사용 방법
### 프로젝트 초기화
```
mkdir ./storyai_example
cd ,/storyai_example
storyai init

openai_api_key: <your openai api key>
```
### 캐릭터 생성
```
storyai persona add

Name: <character's name>
Age: <character's age>
MBTI: <character's MBTI>
Gender: <character's Gender(MALE or FEMALE)>
Description: <character's description(optional)>

Added persona ID: ...
```
### 시놉시스 생성
```
storyai synopsis add

Theme: <theme>
Persona ID: <persona id>
```
### 생성된 시놉시스 조회
```
storyai synopsis show --synopsis-id=<synopsis id>

Synopsis:
  ...
```