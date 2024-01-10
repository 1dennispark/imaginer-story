'use client';

import Button from "@/components/Button";
import Dropdown, { DropdownItem } from "@/components/Dropdown"
import Input from "@/components/Input";
import Notification, { NotificationProps } from "@/components/Notification";
import { Character } from "@/types/db";
import { AGE_RANGE_ITEMS, GENDER_ITEMS, MAX_IMAGE_LIST_LENGTH, MAX_PRESET_LIST_LENGTH, MBTI_ITEMS, MIN_IMAGE_LIST_LENGTH } from "@/util/constants";
import { PlusCircleIcon, XCircleIcon } from "@heroicons/react/20/solid";
import { createClient } from "@supabase/supabase-js";
import { ChangeEvent, useEffect, useRef, useState } from "react";

export default function CharacterPage() {
    const supabase = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL ?? "", process.env.NEXT_PUBLIC_SUPABASE_KEY ?? "");
    const [notify, setNotify] = useState<NotificationProps>({ type: "success", message: "" });
    const inputRef = useRef<HTMLInputElement | null>(null);

    const [characterName, setCharacterName] = useState<string | null>(null);
    const [characterDescription, setCharacterDescription] = useState<string | null>(null);
    const [selectedMBTI, setSelectedMBTI] = useState<string>('');
    const [selectedGender, setSelectedGender] = useState<string>('');
    const [selectedAgeRange, setSelectedAgeRange] = useState<string>('');
    const [selectedImageList, setSelectedImageList] = useState<string[]>([]);

    const [generatedCharacter, setGeneratedCharacter] = useState<Character | null>(null);
    const [presetList, setPresetList] = useState<Character[]>([]);
    const [dataLoading, setDataLoading] = useState<boolean>(true);
    const [apiLoading, setApiLoading] = useState<boolean>(false);

    useEffect(() => {
        const getPresetData = async () => {
            try {
                const { data, error } = await supabase.from("character")
                    .select("*")
                    .order("id", { ascending: false })
                    .range(0, MAX_PRESET_LIST_LENGTH - 1);

                if (error) {
                    setNotify({ type: "error", message: "데이터를 불러오는것에 실패했습니다." });
                    return;
                }
                setPresetList(data);
            } finally {
                setDataLoading(false);
            }
        }

        getPresetData();
    }, []);

    const handleSelectDropdown = (key: string, item: DropdownItem) => {
        if (key == 'mbti') setSelectedMBTI(item.value);
        if (key == 'gender') setSelectedGender(item.value);
        if (key == 'age_range') setSelectedAgeRange(item.value);
    }

    const handleSelectPreset = (preset: Character) => {
        setCharacterName(preset.name);
        setSelectedMBTI(preset.mbti);
        setSelectedGender(preset.gender);
        setSelectedAgeRange(preset.age);
        setCharacterDescription(preset.description);
        setSelectedImageList(preset.original_images ?? []);
    }

    const handleGenerateCharacter = () => {
        if (!checkValidation()) return;
        setApiLoading(true);

        try {
            // TODO: 캐릭터 프로필 생성 API로 변경되어야 함.
            const newCharacter: Character = {
                id: 0,
                name: characterName ?? '',
                mbti: selectedMBTI,
                gender: selectedGender,
                age: selectedAgeRange,
                description: characterDescription ?? '',
                profile_image: selectedImageList[0] ?? '',
                original_images: selectedImageList,
            }
            setGeneratedCharacter(newCharacter);
        } catch (e) {
            setNotify({ type: "error", message: "캐릭터 프로필 생성에 실패했습니다." });
        } finally {
            setApiLoading(false);
        }
    }

    const handleSavePreset = async () => {
        if (!generatedCharacter) return;
        setApiLoading(true);

        try {
            const { data, error } = await supabase
                .from('character')
                .insert({
                    name: generatedCharacter.name,
                    mbti: generatedCharacter.mbti,
                    gender: generatedCharacter.gender,
                    age: generatedCharacter.age,
                    description: generatedCharacter.description,
                    profile_image: generatedCharacter.profile_image,
                    original_images: generatedCharacter.original_images,
                })
                .select();

            if (error) {
                setNotify({ type: "error", message: "프리셋 저장에 실패했습니다." });
                return;
            }

            if (presetList.length >= MAX_PRESET_LIST_LENGTH) {
                setPresetList([data[0], ...presetList].slice(0, MAX_PRESET_LIST_LENGTH));
            } else {
                setPresetList([data[0], ...presetList]);
            }
        } finally {
            setApiLoading(false);
        }
    }

    const handleUploadFile = async (e: ChangeEvent<HTMLInputElement>) => {
        if (!e.target.files) return;
        setApiLoading(true);

        let newImages = [];
        try {
            for (let i = 0; i < e.target.files.length; i++) {
                const fileName = makeid(10);
                const file = e.target.files[i];
                const { error } = await supabase.storage
                    .from("images")
                    .upload(fileName, file, {
                        cacheControl: "3600",
                        upsert: false,
                    });
                if (error) throw error;

                newImages.push(fileName);
            }

            setSelectedImageList([...newImages, ...selectedImageList].slice(0, MAX_IMAGE_LIST_LENGTH));
        } catch (e) {
            setNotify({ type: "error", message: "사진 업로드에 실패했습니다." });
        } finally {
            setApiLoading(false);
        }
    }

    const makeid = (length: number) => {
        let result = "";
        const characters =
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
        const charactersLength = characters.length;
        for (var i = 0; i < length; i++) {
            result += characters.charAt(Math.floor(Math.random() * charactersLength));
        }
        return result;
    }

    const handleDeleteImage = (index: number) => {
        setSelectedImageList(selectedImageList.filter((_, i) => i != index));
    }

    const checkValidation = () => {
        if (!characterName) {
            setNotify({ type: "warning", message: "캐릭터 이름을 입력해주세요." });
            return false;
        }
        if (!characterDescription) {
            setNotify({ type: "warning", message: "캐릭터 설명을 입력해주세요." });
            return false;
        }
        if (!selectedMBTI) {
            setNotify({ type: "warning", message: "MBTI를 선택해주세요." });
            return false;
        }
        if (!selectedGender) {
            setNotify({ type: "warning", message: "성별을 선택해주세요." });
            return false;
        }
        if (!selectedAgeRange) {
            setNotify({ type: "warning", message: "나이대를 선택해주세요." });
            return false;
        }
        if (selectedImageList.length < MIN_IMAGE_LIST_LENGTH) {
            setNotify({ type: "warning", message: "이미지를 6개 이상 업로드해주세요." });
            return false;
        }
        return true;
    }

    return (
        <div className="mt-9">
            <Notification type={notify.type} message={notify.message} />
            <div className="font-bold text-4xl text-black mb-12">캐릭터 프로필 만들기</div>
            <div className="flex gap-x-20 px-5">
                <div className="w-[620px] flex flex-col gap-y-12">
                    <div className="flex gap-x-8">
                        {dataLoading &&
                            <>
                                <div className="animate-pulse w-[85px] h-[30px] shadow-sm rounded-md bg-gray-300 ring-1 ring-inset ring-gray-300" />
                                <div className="animate-pulse w-[85px] h-[30px] shadow-sm rounded-md bg-gray-300 ring-1 ring-inset ring-gray-300" />
                                <div className="animate-pulse w-[85px] h-[30px] shadow-sm rounded-md bg-gray-300 ring-1 ring-inset ring-gray-300" />
                                <div className="animate-pulse w-[85px] h-[30px] shadow-sm rounded-md bg-gray-300 ring-1 ring-inset ring-gray-300" />
                            </>
                        }
                        {!dataLoading && presetList.map((preset, index) => {
                            return (
                                <button key={`preset_${preset.name}_${index}`} className="px-4 py-[5px] shadow-sm rounded-md bg-white font-semibold text-sm text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
                                    onClick={() => handleSelectPreset(preset)} disabled={apiLoading}>
                                    {preset.name}#{preset.id}
                                </button>
                            )
                        })}
                    </div>
                    <div>
                        <div className="font-bold text-2xl text-gray-900 mb-[11px]">원본 이미지 업로드</div>
                        <div className="flex gap-x-[5px] overflow-x-auto">
                            <input
                                multiple
                                type="file"
                                accept="image/*,.heic,.heif"
                                onChange={handleUploadFile}
                                className="hidden"
                                ref={(el) => inputRef.current = el} />
                            <button className="flex w-[100px] h-[100px] items-center justify-center border border-indigo-600 rounded-xl shrink-0" onClick={() => inputRef.current?.click()} disabled={apiLoading}>
                                <PlusCircleIcon className="h-8 w-8 text-indigo-600" aria-hidden="true" />
                            </button>
                            {selectedImageList.map((image, index) => {
                                return (
                                    <button key={`selected_img_${index}`} className="w-[100px] h-[100px] rounded-xl shrink-0 overflow-hidden relative" onClick={() => handleDeleteImage(index)}>
                                        <img className="w-full h-full object-cover" src={`${process.env.NEXT_PUBLIC_SUPABASE_URL}/storage/v1/object/public/images/${image}`} />
                                        <div className="absolute inset-0 bg-white bg-opacity-50 flex items-center justify-center opacity-0 hover:opacity-100">
                                            <div className="w-8 h-8 text-indigo-600"><XCircleIcon /></div>
                                        </div>
                                    </button>
                                )
                            })}
                        </div>
                    </div>
                    <div>
                        <div className="font-bold text-2xl text-gray-900 mb-[11px]">페르소나</div>
                        <div className="flex flex-col gap-y-5">
                            <div className="flex items-center">
                                <div className="w-[72px] text-base font-semibold shrink-0">이름</div>
                                <Input placeholder="캐릭터 이름을 입력해주세요" value={characterName ?? ''} onChange={(e) => { setCharacterName(e.target.value) }} disabled={apiLoading} />
                            </div>
                            <div className="flex gap-x-[35px]">
                                <div className="flex items-center">
                                    <div className="w-[72px] text-base font-semibold shrink-0">MBTI</div>
                                    <Dropdown items={MBTI_ITEMS} placeholder="MBTI" selectedValue={selectedMBTI} onSelected={(item) => { handleSelectDropdown('mbti', item) }} disabled={apiLoading} />
                                </div>
                                <div className="flex items-center">
                                    <div className="w-[72px] text-base font-semibold shrink-0">성별</div>
                                    <Dropdown items={GENDER_ITEMS} placeholder="성별" selectedValue={selectedGender} onSelected={(item) => { handleSelectDropdown('gender', item) }} disabled={apiLoading} />
                                </div>
                                <div className="flex items-center">
                                    <div className="w-[72px] text-base font-semibold shrink-0">나이대</div>
                                    <Dropdown items={AGE_RANGE_ITEMS} placeholder="나이대" selectedValue={selectedAgeRange} onSelected={(item) => { handleSelectDropdown('age_range', item) }} disabled={apiLoading} />
                                </div>
                            </div>
                            <div className="flex items-start">
                                <div className="w-[72px] text-base font-semibold shrink-0">설명</div>
                                <div className="w-full">
                                    <Input textArea placeholder="캐릭터 설명을 입력해주세요" value={characterDescription ?? ''} onChange={(e) => { setCharacterDescription(e.target.value) }} disabled={apiLoading} />
                                </div>
                            </div>
                        </div>
                        <div className="mt-6 text-right">
                            <Button label="실행" onClick={() => handleGenerateCharacter()} loading={apiLoading} />
                        </div>
                    </div>
                </div>
                <div className="w-[340px] flex flex-col">
                    <div className="font-bold text-2xl text-gray-900 mb-[10px]">캐릭터 프로필 카드</div>
                    <div className="flex mb-5 items-center">
                        {generatedCharacter?.profile_image &&
                            <div className="w-[100px] h-[100px] rounded-xl shrink-0 overflow-hidden">
                                <img className="w-full h-full object-cover" src={`${process.env.NEXT_PUBLIC_SUPABASE_URL}/storage/v1/object/public/images/${generatedCharacter.profile_image}`} />
                            </div>
                        }
                        <div className="flex flex-col ml-10">
                            <div className="font-semibold text-xl text-gray-900 mb-5">{generatedCharacter?.name}</div>
                            <div className="flex flex-col gap-y-2 font-normal text-base/[19px] text-gray-900">
                                <div>{generatedCharacter?.mbti}</div>
                                <div>{generatedCharacter?.gender}</div>
                                <div>{generatedCharacter?.age}</div>
                            </div>
                        </div>
                    </div>
                    <div className="font-normal text-base text-gray-900">
                        {generatedCharacter?.description}
                    </div>
                    <div className="text-right mt-6">
                        <Button label="저장" onClick={handleSavePreset} loading={apiLoading} disabled={!generatedCharacter} />
                    </div>
                </div>
            </div>
        </div>
    )
}