import sys
from pathlib import Path
sys.path.append(str(Path(".").absolute().parent))
# sys.path.append("../")
from codetf.models import load_model_pipeline


model_class = load_model_pipeline(model_name="causallm", task="pretrained",
            model_type="codegen-350M-mono", is_eval=True,
            weight_sharding=False)

prompts = "# check if a string is in valid format"
code_snippets = model_class.predict([prompts])

print(code_snippets)