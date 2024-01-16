import Button from "../components/Button";
import Dropdown, {DropdownItem} from "../components/Dropdown";
import Input from "../components/Input";
import Notification, {NotificationProps} from "../components/Notification";
import {Character, Synopsis, SynopsisContent} from "../types";
import {
  API_URL,
  BACKDROP_ITEMS,
  ENDING_ITEMS,
  GENRE_ITEMS,
  MAX_PRESET_LIST_LENGTH,
  MAX_SELECTED_PRESET_LENGTH
} from "../util/constants";
import {CheckCircleIcon, ChevronUpIcon, ChevronDownIcon} from "@heroicons/react/20/solid";
import {useEffect, useState} from "react";
import Layout from "../components/Layout";
import * as apis from "../apis";
import classNames from "classnames";
import ProfileImage from "../components/ProfileImage";


type ChevronIconProps = { up: boolean, className: string, onClick: () => void };

function ChevronIcon({up, className, onClick}: ChevronIconProps) {
  return up ? <ChevronUpIcon className={className} onClick={onClick}/> :
    <ChevronDownIcon className={className} onClick={onClick}/>;
}

function SynopsisMain() {
  const [notify, setNotify] = useState<NotificationProps>({type: "success", message: ""});
  const [selectedPresets, setSelectedPresets] = useState<SynopsisCharacter[]>([]);
  const [selectedGenre, setSelectedGenre] = useState<string>('');
  const [selectedBackdrop, setSelectedBackdrop] = useState<string>('');
  const [selectedEnding, setSelectedEnding] = useState<string>('');
  const [eventDescription, setEventDescription] = useState<string>('');

  const [presets, setPresets] = useState<SynopsisCharacter[]>([]);
  const [synopses, setSynopses] = useState<(SynopsisContent & { open: boolean })[]>([]);
  const [scenario, setScenario] = useState<string>('');
  const [dataLoading, setDataLoading] = useState<boolean>(true);
  const [synopsisLoading, setSynopsisLoading] = useState<boolean>(false);
  const [scenarioLoading, setScenarioLoading] = useState<boolean>(false);

  type SynopsisCharacter = Character & {
    selected: boolean,
  }

  useEffect(() => {
    const getPresetData = async () => {
      try {
        let {data} = await apis.getCharacters();
        if (data.length > MAX_PRESET_LIST_LENGTH) {
          data = data.slice(0, MAX_PRESET_LIST_LENGTH);
        }

        const presets = data.map((character: Character) => {
          return {
            ...character,
            selected: false,
          } as SynopsisCharacter;
        });

        setPresets(presets);
      } finally {
        setDataLoading(false);
      }
    }

    getPresetData();
  }, []);

  const handleSelectDropdown = (key: string, item: DropdownItem) => {
    if (key === 'genre') setSelectedGenre(item.value);
    if (key === 'backdrop') setSelectedBackdrop(item.value);
    if (key === 'ending') setSelectedEnding(item.value);
  }

  const handleSelectSynopsisCharacter = (character: SynopsisCharacter) => {
    if (character.selected && selectedPresets.length > MAX_SELECTED_PRESET_LENGTH) return;
    if (!character.selected && selectedPresets.length >= MAX_SELECTED_PRESET_LENGTH) return;

    setPresets(presets.map((preset) => {
      if (preset.id === character.id) {
        preset.selected = !preset.selected;
      }
      return preset;
    }));

    setSelectedPresets(presets.filter((preset) => preset.selected === true));
  }

  const handleGenerateSynopsis = async () => {
    if (!checkValidation()) return;
    setSynopsisLoading(true);

    try {
      const synopsis: Synopsis = {
        genre: selectedGenre,
        background: selectedBackdrop,
        ending: selectedEnding,
        event_description: eventDescription,
        character_ids: selectedPresets.map(c => c.id),
      }
      const {data} = await apis.generateSynopsis(synopsis);
      setSynopses(data.map(s => ({...s, open: true})));
    } catch (e) {
      console.error(e);
      setNotify({type: "error", message: "통신에 실패했습니다."});
    } finally {
      setSynopsisLoading(false);
    }
  }

  const handleRegenerateScenario = async () => {
    setScenarioLoading(true);

    try {
      const synopsis: Synopsis = {
        genre: selectedGenre,
        background: selectedBackdrop,
        ending: selectedEnding,
        event_description: eventDescription,
        character_ids: selectedPresets.map(c => c.id),
      }
      const {data} = await apis.generateScenario(synopsis, synopses);
      setScenario(data);
    } catch (e) {
      console.error(e);
      setNotify({type: "error", message: "통신에 실패했습니다."});
    } finally {
      setScenarioLoading(false);
    }
  }

  const checkValidation = () => {
    if (selectedPresets.length < 2) {
      setNotify({type: "warning", message: "캐릭터를 2개 이상 선택해주세요"});
      return false;
    }
    if (!selectedGenre) {
      setNotify({type: "warning", message: "장르를 선택해주세요"});
      return false;
    }
    if (!selectedBackdrop) {
      setNotify({type: "warning", message: "배경을 선택해주세요"});
      return false;
    }
    if (!selectedEnding) {
      setNotify({type: "warning", message: "엔딩을 선택해주세요"});
      return false;
    }
    if (!eventDescription) {
      setNotify({type: "warning", message: "이벤트 서술을 입력해주세요"});
      return false;
    }
    return true;
  }

  if (dataLoading) {
    return null;
  }

  return (
    <div className="mt-9">
      <Notification type={notify.type} message={notify.message} onClose={() => {
        setNotify({type: notify.type, message: ""});
      }}/>
      <div className="font-bold text-4xl text-black mb-12">시놉시스 만들기</div>
      <div className="flex gap-x-20 px-5">
        <div className="w-[620px] flex flex-col gap-y-12">
          <div>
            <div className="font-bold text-2xl text-gray-900 mb-[11px]">캐릭터를 선택해주세요</div>
            <div className="flex gap-x-[5px] overflow-x-auto">
              {presets.map((character, index) => {
                return (
                  <button key={`character_${index}`} className="flex flex-col items-center"
                          onClick={() => {
                            handleSelectSynopsisCharacter(character)
                          }}>
                    <div
                      className="w-[100px] h-[100px] rounded-xl shrink-0 overflow-hidden border-2 hover:border-indigo-600 relative">
                      <ProfileImage className="w-full h-full object-cover" character={character} isProse={false} />
                      {character.selected &&
                          <div className="absolute inset-0 bg-white bg-opacity-50 flex items-center justify-center">
                              <div className="w-8 h-8 text-indigo-600"><CheckCircleIcon/></div>
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
                  <Dropdown items={GENRE_ITEMS} placeholder="장르" selectedValue={selectedGenre} onSelected={(item) => {
                    handleSelectDropdown('genre', item)
                  }} disabled={synopsisLoading}/>
                </div>
                <div className="flex items-center">
                  <div className="w-[72px] text-base font-semibold shrink-0">배경</div>
                  <Dropdown items={BACKDROP_ITEMS} placeholder="배경" selectedValue={selectedBackdrop}
                            onSelected={(item) => {
                              handleSelectDropdown('backdrop', item)
                            }} disabled={synopsisLoading}/>
                </div>
                <div className="flex items-center">
                  <div className="w-[72px] text-base font-semibold shrink-0">엔딩</div>
                  <Dropdown items={ENDING_ITEMS} placeholder="엔딩" selectedValue={selectedEnding} onSelected={(item) => {
                    handleSelectDropdown('ending', item)
                  }} disabled={synopsisLoading}/>
                </div>
              </div>
              <div className="flex items-start">
                <div className="w-[115px] text-base font-semibold shrink-0">이벤트 서술<br/>(자유입력)</div>
                <div className="w-full">
                  <Input textArea placeholder="이벤트를 서술해주세요" value={eventDescription} onChange={(e) => {
                    setEventDescription(e.target.value)
                  }} disabled={synopsisLoading}/>
                </div>
              </div>
            </div>
            <div className="mt-6 text-right">
              <Button label="만들기" onClick={() => handleGenerateSynopsis()}
                      loading={synopsisLoading || scenarioLoading}/>
            </div>
          </div>
        </div>
        <div className="w-[340px] flex flex-col gap-y-6">
          <div className="flex flex-col">
            <div className="font-bold text-2xl text-gray-900 mb-[14px]">등장인물</div>
            <div className="flex gap-x-6">
              {selectedPresets.map((character, index) => {
                return (
                  <div key={`character_${index}`} className="flex flex-col items-center">
                    <div className="w-[78px] h-[78px] rounded-xl shrink-0 overflow-hidden">
                      <ProfileImage className="w-full h-full object-cover" character={character} isProse={false}/>
                    </div>
                    <div className="text-sm mt-[6px]">{character.name}</div>
                  </div>
                )
              })}
            </div>
          </div>

          <article className="flex flex-col prose">
            <div className="font-bold text-2xl text-gray-900">시놉시스</div>
            {synopses.map((synopsis, index) => {
              return (
                <>
                  <h3 className="flex flex-row items-center">
                    <ChevronIcon up={!synopsis.open}
                                 className="flex justify-center w-6 h-6 text-gray-400 hover:text-gray-500 hover:cursor-pointer"
                                 onClick={() => {
                                   setSynopses(synopses.map((s, i) => {
                                     if (i === index) {
                                       s.open = !s.open;
                                     }
                                     return s;
                                   }));
                                 }}/>
                    <span key={`synopsis-${index}-title`}
                          className={classNames(
                            "title text-base text-gray-900",
                          )}>{index + 1}장 {synopsis.title}</span>
                  </h3>
                  <p className={classNames({
                    "hidden": !synopsis.open
                  })}>{synopsis.detail}</p>
                </>
              );
            })}
          </article>

          <article className="flex flex-col prose">
            <div className="flex justify-between mb-[14px]">
              <div className="font-bold text-2xl text-gray-900">대화 포함 버전</div>
              <Button label="실행" onClick={() => handleRegenerateScenario()} loading={scenarioLoading}
                      disabled={synopses.length == 0}/>
            </div>
            <p className="font-normal text-base text-gray-900">
              {scenario.split('\n').map(line => {
                return (
                  <>
                    {line}<br/>
                  </>
                );
              })}
            </p>
          </article>
        </div>
      </div>
    </div>
  )
}

export default function SynopsisPage() {
  return (
    <Layout currentPage="synopsis">
      <SynopsisMain/>
    </Layout>
  );
}