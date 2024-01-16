import {Character, CharacterProfileImage, GeneratedContext, SynopsisContent} from "./types";
import axios, {AxiosResponse} from "axios";
import {API_URL} from './util/constants';
import {Synopsis} from "./types";

const client = axios.create({
  baseURL: API_URL,
})

export async function getCharacter(id: number) {
  return client.get<Character>('/personas/' + id);
}

export function addCharacter(character: Character) {
  return client.post<Character>('/personas', character);
}


export function updateCharacter(character: Character): Promise<AxiosResponse<Character>> {
  return client.put<Character>('/personas/' + character.id, character);
}

export function getCharacters(): Promise<AxiosResponse<Character[]>> {
  return client.get<Character[]>('/personas');
}

export function saveImage(file: File) {
  return client.post('/images', {'image': file}, {
    headers: {
      'Content-Type': 'multipart/form-data'
    },
  })
}

export function generateSynopsis(synopsis: Synopsis) {
  return client.post<SynopsisContent[]>('/synopses', synopsis);
}

export function generateScenario(synopsis: Synopsis, contents: SynopsisContent[]) {
  return client.post<string>('/synopses/scenario', {...synopsis, synopses: contents,});
}

export function getProfileImage(id: number) {
  return client.get<CharacterProfileImage>(`/personas/${id}/profile-image`);
}