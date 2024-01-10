import { Character } from "./db";

export type Synopsis = {
    characters: Character[],
    synopses: string[],
    scenario: string,
}