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
  description: string,
  profile_image?: string,
  original_images?: string[],
  context?: string,
};

export type GeneratedContext = {
  context: string,
  profile_image: string,
};