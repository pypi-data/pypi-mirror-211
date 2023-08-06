

from ...core.main import ContinueSDK, Models, Step
from .main import UserInputStep
from .draft.dlt import CreatePipelineStep


step_name_to_step_class = {
    "UserInputStep": UserInputStep,
    "CreatePipelineStep": CreatePipelineStep
}


class StepsOnStartupStep(Step):
    hide: bool = True

    async def describe(self, models: Models):
        return "Running steps on startup"

    async def run(self, sdk: ContinueSDK):
        steps_descriptions = (await sdk.get_config()).steps_on_startup

        for step_name, step_params in steps_descriptions.items():
            try:
                step = step_name_to_step_class[step_name](**step_params)
            except:
                print(
                    f"Incorrect parameters for step {step_name}. Parameters provided were: {step_params}")
                continue
            await sdk.run_step(step)
