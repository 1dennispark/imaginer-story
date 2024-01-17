export type Synopsis = {
  genre: string,
  background: string,
  ending: string,
  character_ids: number[],
  event_description: string,
};

export type SynopsisContent = {
  title: string,
  detail: string,
};

export type Character = {
  id: number,
  name: string,
  mbti: string,
  gender: string,
  age: string,
  job: string,
  description: string,
  original_images: string[],
  profile_image?: string,
  context?: string,
};

export type GeneratedContext = {
  context: string,
  profile_image: string,
};

export type CharacterProfileImage = {
  object_name: string,
  status: string,
};