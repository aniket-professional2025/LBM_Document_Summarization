# Importing Required Packages
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, GenerationConfig
from peft import PeftModel
import warnings
warnings.filterwarnings('ignore')
print("[DEBUG] Imported All Required Packages")

# Model name and Fine-Tuned Path
MODEL_NAME = "meta-llama/Llama-2-7b-chat-hf"  
OUTPUT_DIR = r"C:\Users\Webbies\Jupyter_Notebooks\Assessli_LBM\lora_personalized_lbm"

# Setting the Device
device = "cuda" if torch.cuda.is_available() else "cpu"
print("[DEBUG] The Suitable Device is:", device)

# Creating the Tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast = False)
tokenizer.pad_token = tokenizer.eos_token
print("[DEBUG] Tokenizer Loaded Successfully")

# Loading the Base Model
model_base = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map = "cuda",
    trust_remote_code = True,
    load_in_4bit = True,  
    bnb_4bit_compute_dtype = torch.bfloat16,
    low_cpu_mem_usage = True
)
print("[DEBUG] The Base Model Loaded")

# Load LoRA adapter on top of base model
model = PeftModel.from_pretrained(model_base, OUTPUT_DIR)
model.eval()
print("[DEBUG] The Model is Loaded in Evaluation Mode with Peft")

# Define a function to generate summary
def generate_summary(document: str, user_profile: dict, max_new_tokens = 200):
    profile_str = f"<FOCUS:{user_profile['focus']}> <TONE:{user_profile['tone']}> <LENGTH:{user_profile['length']}> <HISTORY:{'|'.join(user_profile['history'])}>"
    prompt = f"Summarize the following document for a user with preferences: {profile_str}\n\nDocument:\n{document}\n\nSummary:"
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024).to(device)
    gen_config = GenerationConfig(
        temperature=0.2,
        top_p=0.95,
        do_sample=False,
        max_new_tokens=max_new_tokens,
        pad_token_id=tokenizer.eos_token_id
    )
    with torch.no_grad():
        out = model.generate(**inputs, generation_config=gen_config)
    text = tokenizer.decode(out[0], skip_special_tokens=True)
    # post-process: strip prompt prefix
    summary_text = text.split("Summary:")[-1].strip()
    return summary_text

# # Setting the Sample Documentation
# sample_doc = """Nearly 2,000 miners across four states may lose their jobs after yet another major coal company filed for bankruptcy this week
# the third since May and fourth since last October. The bankruptcy filing from Revelation Energy LLC and its affiliate Blackjewel LLC,
# the nation's sixth-top coal producing company in 2017, comes amid President Donald Trump's ongoing efforts to boost the flagging industry.
# The Trump administration rolled out a rule last month aiming to extend the lives of aging coal-fired power plants across the nation.
# Environmentalists say the Affordable Clean Energy rule would trigger premature deaths, including from lung disease. During his 2016
# presidential campaign, Trump promised to revitalize coal and save miners' jobs, despite scientists linking the burning of the fossil fuels
# to global warming , but the industry has continued to suffer losses. Coal comeback? Trump plan breathes new life into aging power plants,
# but critics say climate will suffer At mines and facilities in Virginia, Kentucky, West Virginia and Wyoming, Revelation Energy and
# Blackjewel employ 1,800 workers, according to court documents and The Casper (Wyo.) Star-Tribune . Company officials estimate they owe
# $156 million for goods and services, West Virginia Public Radio reported. Last month, Cambrian Coal LLC also filed for bankruptcy .
# The company operating in Kentucky and Virginia blamed its bankruptcy on changes in demand and regulations related to the Clean Air Act.
# Another coal-producing leader filed for Chapter 11 bankruptcy in May. Once the nation's third-largest coal company, Wyoming-based Cloud Peak Energy
# employed 1,300 people at the time of its filing. It accounted for 7.4% of total U.S. coal production in 2017, according to the Department of Labor .
# And, the nation's ninth-leading coal company went to bankruptcy court late in 2018. Colorado-based Westmoreland Coal Co. had more than $1.4
# billion in debt at the time, The Associated Press reported. Gone by 2030?: On World Environment Day, everything you know about energy in
# the US might be wrong Although Trump has touted coal's rebirth, 51 coal plants have closed and eight coal companies have filed for bankruptcy
# since his election, CBS News reported last month. Coal's share of the U.S. electricity mix fell from 48% in 2008 to 27% in 2018 and is
# projected to be 22% in 2020, according to the Department of Energy. \"We're retiring a coal plant every month. Coal will all be gone by 2030,
# said Bruce Nilles , a managing director at the Rocky Mountain Institute, a think tank in Colorado that focuses on energy and resource efficiency.
# Coal policy, including Trump's Affordable Clean Energy rule , could influence the 2020 election in swing states where coal is still mined,
# such as Ohio and Pennsylvania. Contributing: Beth Weise and Ledyard King, USA TODAY This article originally appeared on USA TODAY:
# Is President Donald Trump losing his fight to save coal? Third major company since May files for bankruptcy.
# """

# print("[DEBUG] Sample Documentation is Set")

# # Build a demo user profile based on the sample_doc content
# demo_profile = {
#     "focus": "results",      # focus on the outcome of the events: job losses, bankruptcies
#     "tone": "analytical",    # factual, professional summary style
#     "length": "medium",      # medium length to capture key points
#     "history": [
#         "Coal industry layoffs in Appalachia",
#         "Bankruptcy filings of major mining companies",
#         "Trump administration energy policies",
#         "Impact of Clean Air Act on coal sector",
#         "US electricity mix and coal decline"
#     ]
# }

# print("Demo user profile:\n", demo_profile)

# demo_profile = {"focus":"results","tone":"analytical","length":"short","history":["previous_article_title_1"]}
# print("Generated summary:\n", generate_summary(sample_doc, demo_profile))