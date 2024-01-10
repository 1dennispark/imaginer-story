'use client';

import Button from "@/components/Button";
import Dropdown, { DropdownItem } from "@/components/Dropdown";
import Input from "@/components/Input";
import Notification, { NotificationProps } from "@/components/Notification";
import { Synopsis } from "@/types/backend";
import { Character } from "@/types/db";
import { BACKDROP_ITEMS, ENDING_ITEMS, GENRE_ITEMS, MAX_PRESET_LIST_LENGTH, MAX_SELECTED_PRESET_LENGTH } from "@/util/constants";
import { CheckCircleIcon } from "@heroicons/react/20/solid";
import { createClient } from "@supabase/supabase-js";
import { useEffect, useState } from "react";

export default function SynopsisPage() {
    const supabase = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL ?? "", process.env.NEXT_PUBLIC_SUPABASE_KEY ?? "");
    const [notify, setNotify] = useState<NotificationProps>({ type: "success", message: "" });
    const [selectedPresetList, setSelectedPresetList] = useState<number[]>([]);
    const [selectedGenre, setSelectedGenre] = useState<string>('');
    const [selectedBackdrop, setSelectedBackdrop] = useState<string>('');
    const [selectedEnding, setSelectedEnding] = useState<string>('');
    const [characterDescription, setCharacterDescription] = useState<string | null>(null);

    const [presetList, setPresetList] = useState<SynopsisCharacter[]>([]);
    const [generatedSynopsis, setGeneratedSynopsis] = useState<Synopsis | null>(null);
    const [dataLoading, setDataLoading] = useState<boolean>(true);
    const [synopsisLoading, setSynopsisLoading] = useState<boolean>(false);
    const [scenarioLoading, setScenarioLoading] = useState<boolean>(false);

    type SynopsisCharacter = Character & {
        selected?: boolean,
    }

    useEffect(() => {
        const getPresetData = async () => {
            try {
                const { data, error } = await supabase.from("character")
                    .select("*")
                    .order("id", { ascending: false });

                if (error) return;
                setPresetList(data);
            } finally {
                setDataLoading(false);
            }
        }

        getPresetData();
    }, []);

    const handleSelectDropdown = (key: string, item: DropdownItem) => {
        if (key == 'genre') setSelectedGenre(item.value);
        if (key == 'backdrop') setSelectedBackdrop(item.value);
        if (key == 'ending') setSelectedEnding(item.value);
    }

    const handleSelectSynopsisCharacter = (character: SynopsisCharacter) => {
        if (character.selected && selectedPresetList.length > MAX_SELECTED_PRESET_LENGTH) return;
        if (!character.selected && selectedPresetList.length >= MAX_SELECTED_PRESET_LENGTH) return;

        setPresetList(presetList.map((preset) => {
            if (preset.id == character.id) {
                preset.selected = !preset.selected;
            }
            return preset;
        }));

        setSelectedPresetList(presetList.filter((preset) => preset.selected == true).map((preset) => preset.id));
    }

    const handleGenerateSynopsis = () => {
        if (!checkValidation()) return;
        setSynopsisLoading(true);

        try {
            // TODO: 시놉시스 생성 API로 변경되어야 함.
            const dummySynopsis: Synopsis = {
                synopses: ['1장', '2장', '3장'],
                characters: [
                    presetList.find((preset) => preset.id == selectedPresetList[0]) as SynopsisCharacter,
                    presetList.find((preset) => preset.id == selectedPresetList[1]) as SynopsisCharacter,
                ],
                scenario: '대화 포함된 시놉시스 내용',
            }

            setGeneratedSynopsis(dummySynopsis);
        } catch (e) {
            setNotify({ type: "error", message: "통신에 실패했습니다." });
        } finally {
            setSynopsisLoading(false);
        }
    }

    const handleRegenerateScenario = () => {
        setScenarioLoading(true);

        try {
            // TODO: 대화 포함된 시놉시스 재생성 API가 추가되어야 함.
        } catch (e) {
            setNotify({ type: "error", message: "통신에 실패했습니다." });
        } finally {
            setScenarioLoading(false);
        }
    }

    const checkValidation = () => {
        if (selectedPresetList.length < 2) {
            setNotify({ type: "warning", message: "캐릭터를 2개 이상 선택해주세요" });
            return false;
        }
        if (!selectedGenre) {
            setNotify({ type: "warning", message: "장르를 선택해주세요" });
            return false;
        }
        if (!selectedBackdrop) {
            setNotify({ type: "warning", message: "배경을 선택해주세요" });
            return false;
        }
        if (!selectedEnding) {
            setNotify({ type: "warning", message: "엔딩을 선택해주세요" });
            return false;
        }
        if (!characterDescription) {
            setNotify({ type: "warning", message: "이벤트 서술을 입력해주세요" });
            return false;
        }
        return true;
    }

    return (
        <div className="mt-9">
            <Notification type={notify.type} message={notify.message} />
            <div className="font-bold text-4xl text-black mb-12">시놉시스 만들기</div>
            <div className="flex gap-x-20 px-5">
                <div className="w-[620px] flex flex-col gap-y-12">
                    <div>
                        <div className="font-bold text-2xl text-gray-900 mb-[11px]">캐릭터를 선택해주세요</div>
                        <div className="flex gap-x-[5px] overflow-x-auto">
                            {dataLoading &&
                                <>
                                    <div className="animate-pulse w-[100px] h-[100px] mb-[26px] bg-gray-300 rounded" />
                                    <div className="animate-pulse w-[100px] h-[100px] mb-[26px] bg-gray-300 rounded" />
                                    <div className="animate-pulse w-[100px] h-[100px] mb-[26px] bg-gray-300 rounded" />
                                    <div className="animate-pulse w-[100px] h-[100px] mb-[26px] bg-gray-300 rounded" />
                                </>
                            }
                            {!dataLoading && presetList.map((character, index) => {
                                return (
                                    <button key={`character_${index}`} className="flex flex-col items-center"
                                        onClick={() => { handleSelectSynopsisCharacter(character) }}>
                                        <div className="w-[100px] h-[100px] rounded-xl shrink-0 overflow-hidden border-2 hover:border-indigo-600 relative">
                                            <img className="w-full h-full object-cover" src={`${process.env.NEXT_PUBLIC_SUPABASE_URL}/storage/v1/object/public/images/${character.profile_image}`} />
                                            {character.selected &&
                                                <div className="absolute inset-0 bg-white bg-opacity-50 flex items-center justify-center">
                                                    <div className="w-8 h-8 text-indigo-600"><CheckCircleIcon /></div>
                                                </div>
                                            }
                                        </div>
                                        <div className="text-sm mt-[6px]">{character.name}</div>
                                    </button>
                                )
                            })}
                        </div>
                    </div>
                    <div>
                        <div className="font-bold text-2xl text-gray-900 mb-[11px]">이벤트 조건</div>
                        <div className="flex flex-col gap-y-5">
                            <div className="flex gap-x-[35px]">
                                <div className="flex items-center">
                                    <div className="w-[72px] text-base font-semibold shrink-0">장르</div>
                                    <Dropdown items={GENRE_ITEMS} placeholder="장르" selectedValue={selectedGenre} onSelected={(item) => { handleSelectDropdown('genre', item) }} disabled={synopsisLoading} />
                                </div>
                                <div className="flex items-center">
                                    <div className="w-[72px] text-base font-semibold shrink-0">배경</div>
                                    <Dropdown items={BACKDROP_ITEMS} placeholder="배경" selectedValue={selectedBackdrop} onSelected={(item) => { handleSelectDropdown('backdrop', item) }} disabled={synopsisLoading} />
                                </div>
                                <div className="flex items-center">
                                    <div className="w-[72px] text-base font-semibold shrink-0">엔딩</div>
                                    <Dropdown items={ENDING_ITEMS} placeholder="엔딩" selectedValue={selectedEnding} onSelected={(item) => { handleSelectDropdown('ending', item) }} disabled={synopsisLoading} />
                                </div>
                            </div>
                            <div className="flex items-start">
                                <div className="w-[115px] text-base font-semibold shrink-0">이벤트 서술<br />(자유입력)</div>
                                <div className="w-full">
                                    <Input textArea placeholder="이벤트를 서술해주세요" value={characterDescription ?? ''} onChange={(e) => { setCharacterDescription(e.target.value) }} disabled={synopsisLoading} />
                                </div>
                            </div>
                        </div>
                        <div className="mt-6 text-right">
                            <Button label="만들기" onClick={() => handleGenerateSynopsis()} loading={synopsisLoading || scenarioLoading} />
                        </div>
                    </div>
                </div>
                <div className="w-[340px] flex flex-col gap-y-6">
                    <div className="flex flex-col">
                        <div className="font-bold text-2xl text-gray-900 mb-[14px]">등장인물</div>
                        <div className="flex gap-x-6">
                            {generatedSynopsis?.characters.map((character, index) => {
                                return (
                                    <div key={`character_${index}`} className="flex flex-col items-center">
                                        <div className="w-[78px] h-[78px] rounded-xl shrink-0 overflow-hidden">
                                            <img className="w-full h-full object-cover" src={`${process.env.NEXT_PUBLIC_SUPABASE_URL}/storage/v1/object/public/images/${character.profile_image}`} />
                                        </div>
                                        <div className="text-sm mt-[6px]">{character.name}</div>
                                    </div>
                                )
                            })}
                        </div>
                    </div>

                    <div className="flex flex-col gap-y-[15px]">
                        <div className="font-bold text-2xl text-gray-900">시놉시스</div>
                        {generatedSynopsis?.synopses.map((synopsis, index) => {
                            return (
                                <div key={`synopsis_${index}`} className="font-normal text-base text-gray-900">
                                    {synopsis}
                                </div>
                            )
                        })}
                    </div>

                    <div className="flex flex-col">
                        <div className="flex justify-between mb-[14px]">
                            <div className="font-bold text-2xl text-gray-900">대화 포함 버전</div>
                            <Button label="실행" onClick={() => handleRegenerateScenario()} loading={scenarioLoading} disabled={!generatedSynopsis} />
                        </div>
                        <div className="font-normal text-base text-gray-900">
                            {generatedSynopsis?.scenario}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}