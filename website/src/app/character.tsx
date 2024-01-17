import Button from "../components/Button";
import Dropdown, {DropdownItem} from "../components/Dropdown"
import Input from "../components/Input";
import Notification, {NotificationProps} from "../components/Notification";
import {Character} from "../types";
import {
  AGE_RANGE_ITEMS,
  API_URL,
  GENDER_ITEMS, JOB_ITEMS,
  MAX_IMAGE_LIST_LENGTH,
  MAX_PRESET_LIST_LENGTH,
  MBTI_ITEMS,
  MIN_IMAGE_LIST_LENGTH,
} from "../util/constants";
import {PlusCircleIcon, XCircleIcon} from "@heroicons/react/20/solid";
import {ChangeEvent, useEffect, useRef, useState} from "react";
import Layout from "../components/Layout";
import * as apis from "../apis";
import ProfileImage from "../components/ProfileImage";
import _ from 'lodash';

function CharacterMain() {
  const [notify, setNotify] = useState<NotificationProps>({type: "success", message: ""});
  const inputRef = useRef<HTMLInputElement | null>(null);

  const [character, setCharacter] = useState<Character>({
    id: 0,
    name: "",
    mbti: "",
    gender: "",
    age: "",
    job: "",
    description: "",
    original_images: [],
  });
  const [presetList, setPresetList] = useState<{name: string, id: number}[]>([]);
  const [dataLoading, setDataLoading] = useState<boolean>(true);
  const [apiLoading, setApiLoading] = useState<boolean>(false);

  useEffect(() => {
    const getPresetData = async () => {
      try {
        let {data} = await apis.getCharacters();
        if (data.length >= MAX_PRESET_LIST_LENGTH) {
          data = data.slice(0, MAX_PRESET_LIST_LENGTH);
        }
        const presets = data.map(({name, id}) => ({name, id}));
        setPresetList(presets);
      } catch (e) {
        console.error(e);
        setNotify({type: "error", message: "데이터를 불러오는것에 실패했습니다."});
        return;
      } finally {
        setDataLoading(false);
      }
    }

    getPresetData();
  }, []);

  const loadCharacter = async (id: number, apiLoading?: boolean) => {
    setApiLoading(apiLoading??true);
    try {
      const {data} = await apis.getCharacter(id);
      setCharacter(data);
    } catch (e) {
      console.error(e);
      setNotify({type: "error", message: "캐릭터 불러오기가 실패했습니다."});
    } finally {
      setApiLoading(false);
    }
  }

  const handleGenerateCharacter = async () => {
    if (!checkValidation()) return;
    setApiLoading(true);

    try {
      const {data} = character.id === 0 ? await apis.addCharacter(character) : await apis.updateCharacter(character);
      setCharacter(data);
      setPresetList([data, ...presetList].slice(0, MAX_PRESET_LIST_LENGTH));
    } catch (e) {
      console.error(e);
      setNotify({type: "error", message: "캐릭터 프로필 생성에 실패했습니다."});
    } finally {
      setApiLoading(false);
    }
  }

  const handleUploadFile = async (e: ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files) return;
    setApiLoading(true);

    try {
      const files = e.target.files;
      const newImages = await Promise.all(_.range(0, e.target.files.length).map(async (i) => {
        const file = files[i];
        const {data: {object_name}} = await apis.saveImage(file);
        return object_name;
      }));

      setCharacter({
        ...character,
        original_images: [...newImages, ...character.original_images].slice(0, MAX_IMAGE_LIST_LENGTH),
      });
    } catch (e) {
      setNotify({type: "error", message: "사진 업로드에 실패했습니다."});
    } finally {
      setApiLoading(false);
    }
  }

  const handleDeleteImage = (index: number) => {
    const original_images = character.original_images.filter((_, i) => i != index);
    setCharacter({...character, original_images});
  }

  const checkValidation = () => {
    if (character.name === "") {
      setNotify({type: "warning", message: "캐릭터 이름을 입력해주세요."});
      return false;
    }
    if (character.description === "") {
      setNotify({type: "warning", message: "캐릭터 설명을 입력해주세요."});
      return false;
    }
    if (character.mbti === "") {
      setNotify({type: "warning", message: "MBTI를 선택해주세요."});
      return false;
    }
    if (character.gender === "") {
      setNotify({type: "warning", message: "성별을 선택해주세요."});
      return false;
    }
    if (character.age === "") {
      setNotify({type: "warning", message: "나이대를 선택해주세요."});
      return false;
    }
    if (character.job === "") {
      setNotify({type: "warning", message: "직업을 선택해주세요."});
      return false;
    }
    if (character.original_images.length < MIN_IMAGE_LIST_LENGTH) {
      setNotify({type: "warning", message: "이미지를 6개 이상 업로드해주세요."});
      return false;
    }
    return true;
  }

  return !dataLoading ? (
    <div className="mt-9">
      <Notification type={notify.type} message={notify.message} onClose={() => {
        setNotify({type: "success", message: ""});
      }}/>
      <div className="font-bold text-4xl text-black mb-12">캐릭터 프로필 만들기</div>
      <div className="flex gap-x-20 px-5">
        <div className="w-[620px] flex flex-col gap-y-12">
          <div className="flex gap-x-6">
            {presetList.map((preset, index) => {
              return (
                <button key={`preset_${preset.name}_${index}`}
                        className="px-4 py-[5px] shadow-sm rounded-md bg-white font-semibold text-sm text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
                        onClick={() => loadCharacter(preset.id)} disabled={apiLoading}>
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
                ref={(el) => inputRef.current = el}/>
              <button className="flex w-[100px] h-[100px] items-center justify-center border border-indigo-600 rounded-xl shrink-0" onClick={() => inputRef.current?.click()}
                      disabled={apiLoading}>
                <PlusCircleIcon className="h-8 w-8 text-indigo-600" aria-hidden="true"/>
              </button>
              {character.original_images.map((image, index) => {
                return (
                  <button key={`selected_img_${index}`} className="w-[100px] h-[100px] rounded-xl shrink-0 overflow-hidden relative" onClick={() => handleDeleteImage(index)}>
                    <img className="w-full h-full object-cover" src={`${API_URL}/images/${image}`} alt=""/>
                    <div className="absolute inset-0 bg-white bg-opacity-50 flex items-center justify-center opacity-0 hover:opacity-100">
                      <div className="w-8 h-8 text-indigo-600"><XCircleIcon/></div>
                    </div>
                  </button>
                );
              })}
            </div>
          </div>
          <div>
            <div className="font-bold text-2xl text-gray-900 mb-[11px]">페르소나</div>
            <div className="flex flex-col gap-y-5">
              <div className="flex items-center">
                <div className="w-[72px] text-base font-semibold shrink-0">이름</div>
                <Input placeholder="캐릭터 이름을 입력해주세요" value={character.name} onChange={(e) => {
                  setCharacter({...character, name: e.target.value});
                }} disabled={apiLoading}/>
              </div>
              <div className="flex items-center">
                <div className="w-[72px] text-base font-semibold shrink-0">직업</div>
                <Dropdown items={JOB_ITEMS} placeholder="직업" selectedValue={character.job} onSelected={({value}) => {
                  setCharacter({...character, job: value});
                }} disabled={apiLoading}/>
              </div>
              <div className="flex gap-x-[35px]">
                <div className="flex items-center">
                  <div className="w-[72px] text-base font-semibold shrink-0">MBTI</div>
                  <Dropdown items={MBTI_ITEMS} placeholder="MBTI" selectedValue={character.mbti} onSelected={({value}) => {
                    setCharacter({...character, mbti: value});
                  }} disabled={apiLoading}/>
                </div>
                <div className="flex items-center">
                  <div className="w-[72px] text-base font-semibold shrink-0">성별</div>
                  <Dropdown items={GENDER_ITEMS} placeholder="성별" selectedValue={character.gender} onSelected={({value}) => {
                    setCharacter({...character, gender: value});
                  }} disabled={apiLoading}/>
                </div>
                <div className="flex items-center">
                  <div className="w-[72px] text-base font-semibold shrink-0">나이대</div>
                  <Dropdown items={AGE_RANGE_ITEMS} placeholder="나이대" selectedValue={character.age} onSelected={({value}) => {
                    setCharacter({...character, age: value});
                  }} disabled={apiLoading}/>
                </div>
              </div>
              <div className="flex items-start">
                <div className="w-[72px] text-base font-semibold shrink-0">설명</div>
                <div className="w-full">
                  <Input textArea placeholder="캐릭터 설명을 입력해주세요" value={character.description} onChange={(e) => {
                    setCharacter({...character, description: e.target.value});
                  }} disabled={apiLoading}/>
                </div>
              </div>
            </div>
            <div className="mt-6 text-right">
              <Button label="실행" onClick={() => handleGenerateCharacter()} loading={apiLoading}/>
            </div>
          </div>
        </div>
        <div className="w-[340px] flex flex-col">
          <div className="font-bold text-2xl text-gray-900 mb-[10px]">캐릭터 프로필 카드</div>
          <article className="prose">
            <div className="flex mb-5 items-center">
              <div className="flex flex-col items-center w-[100px]">
                <ProfileImage className="w-full h-[100px] object-cover rounded-xl" character={character} />
              </div>
              <div className="flex flex-col ml-10">
                <div className="font-semibold text-xl text-gray-900 mb-5">{character.name}</div>
                <div className="flex flex-col gap-y-2 font-normal text-base/[19px] text-gray-900">
                  <div>{character.mbti}</div>
                  <div>{character.gender}</div>
                  <div>{character.age}</div>
                </div>
              </div>
            </div>
            <div className="font-normal text-base text-gray-900">
              <p>
                {character.context?.split('\n').map(line => {
                  return (
                    <>
                      {line}<br/>
                    </>
                  );
                })}
              </p>
            </div>
          </article>
        </div>
      </div>
    </div>
  ) : null;
}

export default function CharacterPage() {
  return (
    <Layout currentPage="character">
      <CharacterMain/>
    </Layout>
  );
}