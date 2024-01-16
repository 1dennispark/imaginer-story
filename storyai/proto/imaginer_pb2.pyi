from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
ERRORED: BoothState
FINISHED: BoothState
READY: BoothState
TRAINING: BoothState

class BoothError(_message.Message):
    __slots__ = ["code", "reason"]
    class Code(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    CODE_FIELD_NUMBER: _ClassVar[int]
    NONE: BoothError.Code
    OBJECT_NOT_FOUND: BoothError.Code
    REASON_FIELD_NUMBER: _ClassVar[int]
    code: BoothError.Code
    reason: str
    def __init__(self, reason: _Optional[str] = ..., code: _Optional[_Union[BoothError.Code, str]] = ...) -> None: ...

class CreateBoothReq(_message.Message):
    __slots__ = ["base_model_name", "booth_class", "class_prompt", "instance_image_uris", "instance_prompt", "params", "storage_password", "version"]
    class BoothClass(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    BASE_MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    BOOTH_CLASS_FIELD_NUMBER: _ClassVar[int]
    CAT: CreateBoothReq.BoothClass
    CLASS_PROMPT_FIELD_NUMBER: _ClassVar[int]
    DOG: CreateBoothReq.BoothClass
    INSTANCE_IMAGE_URIS_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_PROMPT_FIELD_NUMBER: _ClassVar[int]
    MAN: CreateBoothReq.BoothClass
    NONE: CreateBoothReq.BoothClass
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    STORAGE_PASSWORD_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    WOMAN: CreateBoothReq.BoothClass
    base_model_name: str
    booth_class: CreateBoothReq.BoothClass
    class_prompt: str
    instance_image_uris: _containers.RepeatedScalarFieldContainer[str]
    instance_prompt: str
    params: DreamBoothTuningParams
    storage_password: str
    version: str
    def __init__(self, instance_image_uris: _Optional[_Iterable[str]] = ..., instance_prompt: _Optional[str] = ..., base_model_name: _Optional[str] = ..., params: _Optional[_Union[DreamBoothTuningParams, _Mapping]] = ..., class_prompt: _Optional[str] = ..., booth_class: _Optional[_Union[CreateBoothReq.BoothClass, str]] = ..., storage_password: _Optional[str] = ..., version: _Optional[str] = ...) -> None: ...

class CreateBoothResp(_message.Message):
    __slots__ = ["booth_id"]
    BOOTH_ID_FIELD_NUMBER: _ClassVar[int]
    booth_id: int
    def __init__(self, booth_id: _Optional[int] = ...) -> None: ...

class DiffuseReq(_message.Message):
    __slots__ = ["dream_booth_id", "guidance_scale", "high_noise_frac", "lang", "model_name", "negative_prompt", "num_inference_steps", "num_samples", "prompt", "safety", "seed", "style", "use_refiner"]
    DREAM_BOOTH_ID_FIELD_NUMBER: _ClassVar[int]
    GUIDANCE_SCALE_FIELD_NUMBER: _ClassVar[int]
    HIGH_NOISE_FRAC_FIELD_NUMBER: _ClassVar[int]
    LANG_FIELD_NUMBER: _ClassVar[int]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    NEGATIVE_PROMPT_FIELD_NUMBER: _ClassVar[int]
    NUM_INFERENCE_STEPS_FIELD_NUMBER: _ClassVar[int]
    NUM_SAMPLES_FIELD_NUMBER: _ClassVar[int]
    PROMPT_FIELD_NUMBER: _ClassVar[int]
    SAFETY_FIELD_NUMBER: _ClassVar[int]
    SEED_FIELD_NUMBER: _ClassVar[int]
    STYLE_FIELD_NUMBER: _ClassVar[int]
    USE_REFINER_FIELD_NUMBER: _ClassVar[int]
    dream_booth_id: int
    guidance_scale: float
    high_noise_frac: float
    lang: str
    model_name: str
    negative_prompt: str
    num_inference_steps: int
    num_samples: int
    prompt: str
    safety: bool
    seed: int
    style: str
    use_refiner: bool
    def __init__(self, prompt: _Optional[str] = ..., num_samples: _Optional[int] = ..., lang: _Optional[str] = ..., style: _Optional[str] = ..., num_inference_steps: _Optional[int] = ..., negative_prompt: _Optional[str] = ..., safety: bool = ..., dream_booth_id: _Optional[int] = ..., model_name: _Optional[str] = ..., seed: _Optional[int] = ..., guidance_scale: _Optional[float] = ..., high_noise_frac: _Optional[float] = ..., use_refiner: bool = ...) -> None: ...

class DiffuseResp(_message.Message):
    __slots__ = ["ok", "predictions", "seed"]
    OK_FIELD_NUMBER: _ClassVar[int]
    PREDICTIONS_FIELD_NUMBER: _ClassVar[int]
    SEED_FIELD_NUMBER: _ClassVar[int]
    ok: bool
    predictions: _containers.RepeatedCompositeFieldContainer[DiffusionOutput]
    seed: int
    def __init__(self, predictions: _Optional[_Iterable[_Union[DiffusionOutput, _Mapping]]] = ..., ok: bool = ..., seed: _Optional[int] = ...) -> None: ...

class DiffusionOutput(_message.Message):
    __slots__ = ["has_nsfw", "image", "neg_text_fid", "subject_fid", "text_fid"]
    HAS_NSFW_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    NEG_TEXT_FID_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_FID_FIELD_NUMBER: _ClassVar[int]
    TEXT_FID_FIELD_NUMBER: _ClassVar[int]
    has_nsfw: bool
    image: bytes
    neg_text_fid: float
    subject_fid: float
    text_fid: float
    def __init__(self, image: _Optional[bytes] = ..., has_nsfw: bool = ..., subject_fid: _Optional[float] = ..., text_fid: _Optional[float] = ..., neg_text_fid: _Optional[float] = ...) -> None: ...

class DreamBoothTuningParams(_message.Message):
    __slots__ = ["center_crop", "learning_rate", "max_train_steps", "object_align", "object_crop", "padding", "remove_background", "resizing", "seed"]
    class ObjectAlignment(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class Padding(_message.Message):
        __slots__ = ["bottom", "left", "right", "top"]
        BOTTOM_FIELD_NUMBER: _ClassVar[int]
        LEFT_FIELD_NUMBER: _ClassVar[int]
        RIGHT_FIELD_NUMBER: _ClassVar[int]
        TOP_FIELD_NUMBER: _ClassVar[int]
        bottom: int
        left: int
        right: int
        top: int
        def __init__(self, left: _Optional[int] = ..., top: _Optional[int] = ..., right: _Optional[int] = ..., bottom: _Optional[int] = ...) -> None: ...
    CENTER: DreamBoothTuningParams.ObjectAlignment
    CENTER_CROP_FIELD_NUMBER: _ClassVar[int]
    LEARNING_RATE_FIELD_NUMBER: _ClassVar[int]
    MAX_TRAIN_STEPS_FIELD_NUMBER: _ClassVar[int]
    MID_BOTTOM: DreamBoothTuningParams.ObjectAlignment
    OBJECT_ALIGN_FIELD_NUMBER: _ClassVar[int]
    OBJECT_CROP_FIELD_NUMBER: _ClassVar[int]
    PADDING_FIELD_NUMBER: _ClassVar[int]
    REMOVE_BACKGROUND_FIELD_NUMBER: _ClassVar[int]
    RESIZING_FIELD_NUMBER: _ClassVar[int]
    SEED_FIELD_NUMBER: _ClassVar[int]
    center_crop: bool
    learning_rate: float
    max_train_steps: int
    object_align: DreamBoothTuningParams.ObjectAlignment
    object_crop: bool
    padding: DreamBoothTuningParams.Padding
    remove_background: bool
    resizing: bool
    seed: int
    def __init__(self, center_crop: bool = ..., resizing: bool = ..., max_train_steps: _Optional[int] = ..., seed: _Optional[int] = ..., remove_background: bool = ..., padding: _Optional[_Union[DreamBoothTuningParams.Padding, _Mapping]] = ..., object_crop: bool = ..., object_align: _Optional[_Union[DreamBoothTuningParams.ObjectAlignment, str]] = ..., learning_rate: _Optional[float] = ...) -> None: ...

class EndTrainingReq(_message.Message):
    __slots__ = ["booth_id", "error", "model_uri", "succeeded", "training_data_uri"]
    BOOTH_ID_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    MODEL_URI_FIELD_NUMBER: _ClassVar[int]
    SUCCEEDED_FIELD_NUMBER: _ClassVar[int]
    TRAINING_DATA_URI_FIELD_NUMBER: _ClassVar[int]
    booth_id: int
    error: BoothError
    model_uri: str
    succeeded: bool
    training_data_uri: str
    def __init__(self, booth_id: _Optional[int] = ..., succeeded: bool = ..., model_uri: _Optional[str] = ..., training_data_uri: _Optional[str] = ..., error: _Optional[_Union[BoothError, _Mapping]] = ...) -> None: ...

class EndTrainingResp(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetBoothReq(_message.Message):
    __slots__ = ["booth_id"]
    BOOTH_ID_FIELD_NUMBER: _ClassVar[int]
    booth_id: int
    def __init__(self, booth_id: _Optional[int] = ...) -> None: ...

class GetBoothResp(_message.Message):
    __slots__ = ["error", "instance_image_uris", "model_uri", "params", "ssec_key", "state"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_IMAGE_URIS_FIELD_NUMBER: _ClassVar[int]
    MODEL_URI_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    SSEC_KEY_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    error: BoothError
    instance_image_uris: _containers.RepeatedScalarFieldContainer[str]
    model_uri: str
    params: DreamBoothTuningParams
    ssec_key: str
    state: BoothState
    def __init__(self, state: _Optional[_Union[BoothState, str]] = ..., model_uri: _Optional[str] = ..., params: _Optional[_Union[DreamBoothTuningParams, _Mapping]] = ..., instance_image_uris: _Optional[_Iterable[str]] = ..., ssec_key: _Optional[str] = ..., error: _Optional[_Union[BoothError, _Mapping]] = ...) -> None: ...

class PreProcessReq(_message.Message):
    __slots__ = ["class_name", "instance_image_uris", "params", "storage_password"]
    CLASS_NAME_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_IMAGE_URIS_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    STORAGE_PASSWORD_FIELD_NUMBER: _ClassVar[int]
    class_name: str
    instance_image_uris: _containers.RepeatedScalarFieldContainer[str]
    params: DreamBoothTuningParams
    storage_password: str
    def __init__(self, params: _Optional[_Union[DreamBoothTuningParams, _Mapping]] = ..., instance_image_uris: _Optional[_Iterable[str]] = ..., storage_password: _Optional[str] = ..., class_name: _Optional[str] = ...) -> None: ...

class PreProcessResp(_message.Message):
    __slots__ = ["results"]
    class Result(_message.Message):
        __slots__ = ["error_code", "error_reason", "ok", "processed_image"]
        ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
        ERROR_REASON_FIELD_NUMBER: _ClassVar[int]
        OK_FIELD_NUMBER: _ClassVar[int]
        PROCESSED_IMAGE_FIELD_NUMBER: _ClassVar[int]
        error_code: int
        error_reason: str
        ok: bool
        processed_image: bytes
        def __init__(self, ok: bool = ..., processed_image: _Optional[bytes] = ..., error_reason: _Optional[str] = ..., error_code: _Optional[int] = ...) -> None: ...
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[PreProcessResp.Result]
    def __init__(self, results: _Optional[_Iterable[_Union[PreProcessResp.Result, _Mapping]]] = ...) -> None: ...

class TrainingReq(_message.Message):
    __slots__ = ["base_model_name", "booth_id", "class_name", "class_prompt", "instance_image_uris", "instance_prompt", "params", "ssec_key"]
    BASE_MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    BOOTH_ID_FIELD_NUMBER: _ClassVar[int]
    CLASS_NAME_FIELD_NUMBER: _ClassVar[int]
    CLASS_PROMPT_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_IMAGE_URIS_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_PROMPT_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    SSEC_KEY_FIELD_NUMBER: _ClassVar[int]
    base_model_name: str
    booth_id: int
    class_name: str
    class_prompt: str
    instance_image_uris: _containers.RepeatedScalarFieldContainer[str]
    instance_prompt: str
    params: DreamBoothTuningParams
    ssec_key: str
    def __init__(self, booth_id: _Optional[int] = ..., instance_image_uris: _Optional[_Iterable[str]] = ..., instance_prompt: _Optional[str] = ..., base_model_name: _Optional[str] = ..., params: _Optional[_Union[DreamBoothTuningParams, _Mapping]] = ..., class_name: _Optional[str] = ..., class_prompt: _Optional[str] = ..., ssec_key: _Optional[str] = ...) -> None: ...

class TrainingResp(_message.Message):
    __slots__ = ["booth_id", "error", "model_uri", "succeeded", "training_data_uri"]
    BOOTH_ID_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    MODEL_URI_FIELD_NUMBER: _ClassVar[int]
    SUCCEEDED_FIELD_NUMBER: _ClassVar[int]
    TRAINING_DATA_URI_FIELD_NUMBER: _ClassVar[int]
    booth_id: int
    error: BoothError
    model_uri: str
    succeeded: bool
    training_data_uri: str
    def __init__(self, booth_id: _Optional[int] = ..., succeeded: bool = ..., model_uri: _Optional[str] = ..., training_data_uri: _Optional[str] = ..., error: _Optional[_Union[BoothError, _Mapping]] = ...) -> None: ...

class TryBeginTrainingReq(_message.Message):
    __slots__ = ["version"]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    version: str
    def __init__(self, version: _Optional[str] = ...) -> None: ...

class TryBeginTrainingResp(_message.Message):
    __slots__ = ["base_model_name", "booth_id", "class_name", "class_prompt", "instance_image_uris", "instance_prompt", "params", "ssec_key"]
    BASE_MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    BOOTH_ID_FIELD_NUMBER: _ClassVar[int]
    CLASS_NAME_FIELD_NUMBER: _ClassVar[int]
    CLASS_PROMPT_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_IMAGE_URIS_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_PROMPT_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    SSEC_KEY_FIELD_NUMBER: _ClassVar[int]
    base_model_name: str
    booth_id: int
    class_name: str
    class_prompt: str
    instance_image_uris: _containers.RepeatedScalarFieldContainer[str]
    instance_prompt: str
    params: DreamBoothTuningParams
    ssec_key: str
    def __init__(self, booth_id: _Optional[int] = ..., instance_image_uris: _Optional[_Iterable[str]] = ..., instance_prompt: _Optional[str] = ..., base_model_name: _Optional[str] = ..., params: _Optional[_Union[DreamBoothTuningParams, _Mapping]] = ..., class_name: _Optional[str] = ..., class_prompt: _Optional[str] = ..., ssec_key: _Optional[str] = ...) -> None: ...

class UpdateBoothReq(_message.Message):
    __slots__ = ["booth_id", "error", "model_uri", "succeeded", "training_data_uri"]
    BOOTH_ID_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    MODEL_URI_FIELD_NUMBER: _ClassVar[int]
    SUCCEEDED_FIELD_NUMBER: _ClassVar[int]
    TRAINING_DATA_URI_FIELD_NUMBER: _ClassVar[int]
    booth_id: int
    error: BoothError
    model_uri: str
    succeeded: bool
    training_data_uri: str
    def __init__(self, booth_id: _Optional[int] = ..., succeeded: bool = ..., model_uri: _Optional[str] = ..., training_data_uri: _Optional[str] = ..., error: _Optional[_Union[BoothError, _Mapping]] = ...) -> None: ...

class UpdateBoothResp(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class BoothState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
