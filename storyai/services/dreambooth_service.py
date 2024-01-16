import grpc
from sqlalchemy import orm, select

from .. import proto, models, domain
from ..settings import Settings

_INSTANCE_PROMPTS = {
    domain.Gender.MALE: "A sks man",
    domain.Gender.FEMALE: "A sks woman",
}

_CLASS_PROMPTS = {
    domain.Gender.MALE: "A man",
    domain.Gender.FEMALE: "A woman",
}

_BOOTH_CLASSES = {
    domain.Gender.MALE: proto.CreateBoothReq.MAN,
    domain.Gender.FEMALE: proto.CreateBoothReq.WOMAN,
}


class DreamBoothService(object):
    def __init__(
            self,
            db: orm.Session,
            settings: Settings,
            ctrl: proto.DreamBoothControllerStub,
            diffuser: proto.DiffuserStub,
    ):
        self._ctrl = ctrl
        self._diffuser = diffuser
        self._image_bucket_name = settings.oci_bucket_name
        self._image_bucket_namespace = settings.oci_bucket_namespace
        self._db = db

    def get_prompt_base(self, job: str):
        prompt = self._db.execute(select(domain.Prompt).where(domain.Prompt.job == job)).scalar_one()
        return {
            'negative': prompt.negative_prompt,
            domain.Gender.MALE: prompt.male_prompt,
            domain.Gender.FEMALE: prompt.female_prompt,
        }

    @property
    def dreambooth_tuning_params(self):
        return proto.DreamBoothTuningParams(
            center_crop=False,
            resizing=False,
            seed=767177526,
            remove_background=True,
            padding=proto.DreamBoothTuningParams.Padding(
                top=90,
                right=45,
                bottom=0,
                left=45,
            ),
            object_crop=True,
            object_align=proto.DreamBoothTuningParams.MID_BOTTOM,
            learning_rate=5e-6,
            max_train_steps=300,
        )

    def create_booth(
            self,
            instance_image_objects: list[str],
            gender: domain.Gender,
    ) -> int:
        image_urls = []
        for object_name in instance_image_objects:
            image_url = f"ocios://{self._image_bucket_name}/{self._image_bucket_namespace}/images/{object_name}"
            image_urls.append(image_url)

        resp: proto.CreateBoothResp = self._ctrl.CreateBooth(proto.CreateBoothReq(
            instance_image_uris=image_urls,
            instance_prompt=_INSTANCE_PROMPTS[gender],
            base_model_name="paust/stable-diffusion-v1-5",
            params=self.dreambooth_tuning_params,
            class_prompt=_CLASS_PROMPTS[gender],
            booth_class=_BOOTH_CLASSES[gender],
            storage_password=None,
            version="1.0",
        ))

        return resp.booth_id

    def get_booth(
            self,
            booth_id: int,
    ) -> (proto.BoothState, proto.BoothError):
        resp: proto.GetBoothResp = self._ctrl.GetBooth(proto.GetBoothReq(
            booth_id=booth_id,
        ))
        return resp.state, resp.error

    def diffuse_booth(
            self,
            booth_id: int,
            job: str,
            gender: domain.Gender,
    ) -> bytes:
        prompt_base = self.get_prompt_base(job)
        neg_prompt = prompt_base['negative']
        prompt = prompt_base[gender]
        resp: proto.DiffuseResp = self._diffuser.Diffuse(proto.DiffuseReq(
            prompt=prompt,
            num_samples=1,
            negative_prompt=neg_prompt,
            model_name='stable-diffusion-v1-5',
            dream_booth_id=booth_id,
        ))

        return resp.predictions[0].image
