export type Character = {
  id: number,
  name: string,
  mbti: string,
  gender: string,
  age: string,
  description: string,
  profile_image?: string,
  original_images? : string[],
}