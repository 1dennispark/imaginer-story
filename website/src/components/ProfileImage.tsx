import {useEffect, useRef, useState} from "react";
import * as apis from '../apis';
import {API_URL} from "../util/constants";
import {LoadingCircle} from "./Icons";
import classNames from "classnames";
import {Character} from "../types";

type ProfileImageProps = {
  character: Character;
  className: string;
  isProse?: boolean;
}

export default function ProfileImage({character, className, isProse}: ProfileImageProps) {
  const [src, setSrc] = useState("");
  const [status, setStatus] = useState("none");
  const [timeoutId, setTimeoutId] = useState<any|null>(null);

  isProse = isProse??true;

  useEffect(() => {
    const loadProfileImage = async () => {
      if (character.id === 0) {
        return;
      }

      setStatus("loading");
      if (timeoutId != null) {
        clearTimeout(timeoutId);
      }

      try {
        const {data: {object_name, status}} = await apis.getProfileImage(character.id);
        if (status === "ok") {
          setSrc(`${API_URL}/images/${object_name}`);
        } else if (status === "errored") {
          setSrc("/images/warning-sign-9763.svg");
        } else {
          setTimeoutId(setTimeout(loadProfileImage, 3500));
        }
        setStatus(status);
      } catch (e) {
        console.log(e);
      }
    };

    loadProfileImage();
  }, [character]);

  switch (status) {
    case "loading":
      return <div className={classNames(
        className,
        {
          'mt-8 mb-8': isProse,
        }
        )}>
        <LoadingCircle width="100%" height="100%" color="fill-black" />
      </div>;
    case "none":
      return null;
    default:
      return <img src={src} alt="" className={className}/>;
  }
}