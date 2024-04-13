# << OSWorld>> 
## OSWorld File Tree

```
OSWorld/
    CONTRIBUTION.md
    lib_run_single.py
    main.py
    README.md
    ROADMAP.md
    run.py
    settings.json
    setup_vm.py
    show_result.py
    desktop_env/
        README.md
        __init__.py
        assets/
        controllers/
            python.py
            setup.py
            __init__.py
        envs/
            actions.py
            desktop_env.py
            __init__.py
        evaluators/
            README.md
            __init__.py
        server/
            main.py
            osbench_server.service
            osbench_server@.service
            pyxcursor.py
            README.md
    evaluation_examples/
        README.md
        test_all.json
        test_small.json
        examples/
            template.json
        settings/
    mm_agents/
        agent.py
        prompts.py
        README.md
        __init__.py
        accessibility_tree_wrap/
            heuristic_retrieve.py
            relevant_retrieve.py
            __init__.py
        gui_som/
            READAME.md
            __init__.py
        llm_server/

```

## CONTRIBUTION.md

```markdown

```

## lib_run_single.py

```python
import datetime
import json
import logging
import os
# import wandb

from wrapt_timeout_decorator import *

logger = logging.getLogger("desktopenv.experiment")

# Open the JSON file
with open("./settings.json", "r") as file:
    # Load the JSON data from the file
    data = json.load(file)
time_limit = data["time_limit"]

@timeout(time_limit, use_signals=False)
def run_single_example(agent, env, example, max_steps, instruction, args, example_result_dir, scores):
    agent.reset()
    obs = env.reset(task_config=example)
    done = False
    step_idx = 0
    env.controller.start_recording()
    # str_table = wandb.Table(columns=["Screenshot", "A11T", "Modle Response", "Action", "Action timestamp", "Done"])
    while not done and step_idx < max_steps:
        response, actions = agent.predict(
            instruction,
            obs
        )
        for action in actions:
            # Capture the timestamp before executing the action
            action_timestamp = datetime.datetime.now().strftime("%Y%m%d@%H%M%S")
            logger.info("Step %d: %s", step_idx + 1, action)
            obs, reward, done, info = env.step(action, args.sleep_after_execution)

            logger.info("Reward: %.2f", reward)
            logger.info("Done: %s", done)
            # Save screenshot and trajectory information
            with open(os.path.join(example_result_dir, f"step_{step_idx + 1}_{action_timestamp}.png"),
                      "wb") as _f:
                with open(obs['screenshot'], "rb") as __f:
                    screenshot = __f.read()
                _f.write(screenshot)
            # get a11tree and save to wandb
            # thisrun_a11tree = env.controller.get_accessibility_tree()
            # str_table.add_data(wandb.Image(data_or_path=os.path.join(example_result_dir, f"step_{step_idx + 1}_{action_timestamp}.png"), caption=f"step_{step_idx + 1}_{action_timestamp}"),
            #                 thisrun_a11tree,
            #                 response, action, action_timestamp, done)
            # run.log({"Reward": reward})
            with open(os.path.join(example_result_dir, "traj.jsonl"), "a") as f:
                f.write(json.dumps({
                    "step_num": step_idx + 1,
                    "action_timestamp": action_timestamp,
                    "action": action,
                    "reward": reward,
                    "done": done,
                    "info": info,
                    "screenshot_file": f"step_{step_idx + 1}_{action_timestamp}.png"
                }))
                f.write("\n")
            if done:
                logger.info("The episode is done.")
                break
        step_idx += 1
    # run.log({"str_trajectory": str_table})
    result = env.evaluate()
    logger.info("Result: %.2f", result)
    scores.append(result)
    with open(os.path.join(example_result_dir, "result.txt"), "w", encoding="utf-8") as f:
        f.write(f"{result}\n")
    env.controller.end_recording(os.path.join(example_result_dir, "recording.mp4"))
    # run.log({"Result": result})

```

## main.py

```python
import datetime
import json
import logging
import os
import sys
import time
import argparse
from desktop_env.envs.desktop_env import DesktopEnv

#  Logger Configs {{{ # 
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

datetime_str: str = datetime.datetime.now().strftime("%Y%m%d@%H%M%S")

file_handler = logging.FileHandler(os.path.join("logs", "normal-{:}.log".format(datetime_str)), encoding="utf-8")
debug_handler = logging.FileHandler(os.path.join("logs", "debug-{:}.log".format(datetime_str)), encoding="utf-8")
stdout_handler = logging.StreamHandler(sys.stdout)
sdebug_handler = logging.FileHandler(os.path.join("logs", "sdebug-{:}.log".format(datetime_str)), encoding="utf-8")

file_handler.setLevel(logging.INFO)
debug_handler.setLevel(logging.DEBUG)
stdout_handler.setLevel(logging.INFO)
sdebug_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    fmt="\x1b[1;33m[%(asctime)s \x1b[31m%(levelname)s \x1b[32m%(module)s/%(lineno)d-%(processName)s\x1b[1;33m] \x1b[0m%(message)s")
file_handler.setFormatter(formatter)
debug_handler.setFormatter(formatter)
stdout_handler.setFormatter(formatter)
sdebug_handler.setFormatter(formatter)

stdout_handler.addFilter(logging.Filter("desktopenv"))
sdebug_handler.addFilter(logging.Filter("desktopenv"))

logger.addHandler(file_handler)
logger.addHandler(debug_handler)
logger.addHandler(stdout_handler)
logger.addHandler(sdebug_handler)
#  }}} Logger Configs # 

logger = logging.getLogger("desktopenv.main")


def human_agent():
    """
    Runs the Gym environment with human input.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', type=str, default=r"C:\Users\tianbaox\Documents\Virtual Machines\Ubuntu3\Ubuntu3.vmx", help="Path to the virtual machine .vmx file.")
    parser.add_argument('-s', '--snapshot', type=str, default='init_state', help="Name of the snapshot to restore.")
    parser.add_argument('-e', '--example', type=str, help="Path to the example json file.")
    args = parser.parse_args(sys.argv[1:])

    example_path = args.example if args.example is not None and os.path.exists(args.example) else \
        'evaluation_examples/examples/multi_apps/5990457f-2adb-467b-a4af-5c857c92d762.json'
    with open(example_path, "r", encoding="utf-8") as f:
        example = json.load(f)
        if args.snapshot is not None:
            example['snapshot'] = args.snapshot

    assert os.path.exists(args.path), "The specified path to the .vmx file does not exist."
    env = DesktopEnv(
        path_to_vm=args.path,
        snapshot_name=args.snapshot,
        action_space="computer_13"
    )
    # reset the environment to certain snapshot
    observation = env.reset(task_config=example)
    done = False
    logger.info('\x1b[32m[TASK INSTRUCTION]: \x1b[32;3m%s\x1b[0m', example["instruction"])

    input("Press Enter to start human operation...")
    human_start_time = time.time()
    input("Press Enter to finish human operation.")
    print("Time elapsed of human operation: %.2f" % (time.time() - human_start_time))

    result = env.evaluate()
    logger.info("Result: %.2f", result)

    # env.close()
    logger.info("Environment closed.")


if __name__ == "__main__":
    human_agent()

```

## README.md

```markdown
<p align="center">
  <img src="https://huggingface.co/datasets/xlangai/assets/resolve/main/github_banner_v2.png" alt="Banner">
</p>

<p align="center">
  <a href="https://os-world.github.io/">Website</a> •
  <a href="https://arxiv.org/abs/2404.07972">Paper</a> •
  <a href="https://github.com/xlang-ai/OSWorld/tree/main/evaluation_examples">Data</a> •
  <a href="https://os-world.github.io/explorer.html">Data Viewer</a> •
  <a href="https://discord.gg/4Gnw7eTEZR">Discord</a>
</p>

## 📢 Updates
- 2024-04-11: We released our [paper](https://arxiv.org/abs/2404.07972), [environment and benchmark](https://github.com/xlang-ai/OSWorld), and [project page](https://os-world.github.io/). Check it out!

## 💾 Installation
### On Your Desktop or Server (Non-Virtualized Platform)
Suppose you are operating on a system that has not been virtualized, meaning you are not utilizing a virtualized environment like AWS, Azure, or k8s. If this is the case, proceed with the instructions below. However, if you are on a virtualized platform, please refer to the [virtualized platform](https://github.com/xlang-ai/OSWorld?tab=readme-ov-file#virtualized-platform) section.

1. First, clone this repository and `cd` into it. Then, install the dependencies listed in `requirements.txt`. It is recommended that you use the latest version of Conda to manage the environment, but you can also choose to manually install the dependencies. Please ensure that the version of Python is >= 3.9.
	```bash
	# Clone the OSWorld repository
	git clone https://github.com/xlang-ai/OSWorld
	
	# Change directory into the cloned repository
	cd OSWorld
	
	# Optional: Create a Conda environment for OSWorld
	# conda create -n osworld python=3.9
	# conda activate osworld
	
	# Install required dependencies
	pip install -r requirements.txt
	```

Alternatively, you can install the environment without any benchmark tasks:
	```bash
	pip install desktop-env
	```

2. Install [VMware Workstation Pro](https://www.vmware.com/products/workstation-pro/workstation-pro-evaluation.html) (for systems with Apple Chips, you should install [VMware Fusion](https://www.vmware.com/go/getfusion)) and configure the `vmrun` command. Verify the successful installation by running the following:
	```bash
	vmrun -T ws list
	```
If the installation along with the environment variable set is successful, you will see the message showing the current running virtual machines.

3. Run our setup script to download the necessary virtual machines and set up the environment☕:
	```bash
	python setup_vm.py
	```

### On AWS or Azure (Virtualized platform)
We are working on supporting it 👷. Please hold tight!

## 🚀 Quick Start
Run the following minimal example to interact with the environment:
	```python
	from desktop_env.envs.desktop_env import DesktopEnv
	
	example = {
	    "id": "94d95f96-9699-4208-98ba-3c3119edf9c2",
	    "instruction": "I want to install Spotify on my current system. Could you please help me?",
	    "config": [
	        {
	            "type": "execute",
	            "parameters": {
	                "command": [
	                    "python",
	                    "-c",
	                    "import pyautogui; import time; pyautogui.click(960, 540); time.sleep(0.5);"
	                ]
	            }
	        }
	    ],
	    "evaluator": {
	        "func": "check_include_exclude",
	        "result": {
	            "type": "vm_command_line",
	            "command": "which spotify"
	        },
	        "expected": {
	            "type": "rule",
	            "rules": {
	                "include": ["spotify"],
	                "exclude": ["not found"]
	            }
	        }
	    }
	}
	
	env = DesktopEnv(
	    path_to_vm=r"Ubuntu/DesktopEnv-Ubuntu 64-bit Arm.vmx",
	    action_space="pyautogui"
	)
	
	obs = env.reset(task_config=example)
	obs, reward, done, info = env.step("pyautogui.rightClick()")
	```
You will see all the logs of the system running normally, including the successful creation of the environment, completion of setup, and successful execution of actions. In the end, you will observe a successful right-click on the screen, which means you are ready to go.

## 🧪 Experiments
### Agent Baselines
If you wish to run the baseline agent used in our paper, you can execute the following command as an example under the GPT-4V pure-screenshot setting:
	```bash
	python run.py --path_to_vm Ubuntu/Ubuntu.vmx --headless --observation_type screenshot --model gpt-4-vision-preview --result_dir ./results
	```
The results, which include screenshots, actions, and video recordings of the agent's task completion, will be saved in the `./results` directory in this case. You can then run the following command to obtain the result:
	```bash
	python show_result.py
	```

### Evaluation
Please start by reading through the [agent interface](https://github.com/xlang-ai/OSWorld/blob/main/mm_agents/README.md) and the [environment interface](https://github.com/xlang-ai/OSWorld/blob/main/desktop_env/README.md).
Correctly implement the agent interface and import your customized version in the `run.py` file.
Afterward, you can execute a command similar to the one in the previous section to run the benchmark on your agent.

## ❓ FAQ
### What are the running times and costs under different settings?
| Setting                        | Expected Time* | Budget Cost (Full Test Set/Small Test Set) |
| ------------------------------ | -------------- | ------------------------------------------ |
| GPT-4V (screenshot)            | 10h            | $100 ($10)                                 |
| Gemini-ProV (screenshot)       | 15h            | $0 ($0)                                    |
| Claude-3 Opus (screenshot)     | 15h            | $150 ($15)                                 |
| GPT-4V (a11y tree, SoM, etc.)  | 30h            | $500 ($50)                                 |

\*No environment parallelism. Calculated in April 2024.


## 📄 Citation
If you find this environment useful, please consider citing our work:
	```
	@misc{OSWorld,
	      title={OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments}, 
	      author={Tianbao Xie and Danyang Zhang and Jixuan Chen and Xiaochuan Li and Siheng Zhao and Ruisheng Cao and Toh Jing Hua and Zhoujun Cheng and Dongchan Shin and Fangyu Lei and Yitao Liu and Yiheng Xu and Shuyan Zhou and Silvio Savarese and Caiming Xiong and Victor Zhong and Tao Yu},
	      year={2024},
	      eprint={2404.07972},
	      archivePrefix={arXiv},
	      primaryClass={cs.AI}
	}
	```

```

## ROADMAP.md

```markdown
# Road Map
Here we provide a high-level road map for the project. We will update this road map as we make progress.
If you are interested in contributing to the project, please check the [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

## Road Map for Environment Infrastructure

- [x] Explore VMWare, and whether it can be connected and control through mouse package
- [x] Explore Windows and MacOS, whether it can be installed
  - MacOS is closed source and cannot be legally installed
  - Windows is available legally and can be installed
- [x] Build gym-like python interface for controlling the VM
- [x] Recording of actions (mouse movement, click, keyboard) for humans to annotate, and we can replay it and compress it
- [x] Build a simple task, e.g. open a browser, open a website, click on a button, and close the browser
- [x] Set up a pipeline and build agents implementation (zero-shot) for the task
- [x] Start to design on which tasks inside the DesktopENv to focus on, start to wrap up the environment to be public
- [x] Start to annotate the examples for ~~training~~ and testing
- [x] Error handling during file passing and file opening, etc.
- [x] Add accessibility tree from the OS into the observation space
- [x] Add pre-process and post-process action support for benchmarking setup and evaluation
- [x] Experiment logging and visualization system
- [x] Add more tasks, maybe scale to 300 for v1.0.0, and create a dynamic leaderboard
- [x] Multiprocess support, this can enable the reinforcement learning to be more efficient
- [ ] Support running on platform that have nested virtualization, e.g. Google Cloud, AWS, etc. 


## Road Map of Annotation Tool
- [ ] Improve the annotation tool base on DuckTrack, make it more robust which align on accessibility tree
- [ ] Annotate the steps of doing the task
- [ ] Crawl all resources we explored from the internet, and make it easy to access
- [ ] Set up ways for community to contribute new examples

```

## run.py

```python
"""Script to run end-to-end evaluation on the benchmark.
Utils and basic architecture credit to https://github.com/web-arena-x/webarena/blob/main/run.py.
"""
import argparse
import datetime
import json
import logging
import os
import random
import sys
# import wandb

from tqdm import tqdm

import lib_run_single
from desktop_env.envs.desktop_env import DesktopEnv
from mm_agents.agent import PromptAgent

#  Logger Configs {{{ #
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

datetime_str: str = datetime.datetime.now().strftime("%Y%m%d@%H%M%S")

file_handler = logging.FileHandler(os.path.join("logs", "normal-{:}.log".format(datetime_str)), encoding="utf-8")
debug_handler = logging.FileHandler(os.path.join("logs", "debug-{:}.log".format(datetime_str)), encoding="utf-8")
stdout_handler = logging.StreamHandler(sys.stdout)
sdebug_handler = logging.FileHandler(os.path.join("logs", "sdebug-{:}.log".format(datetime_str)), encoding="utf-8")

file_handler.setLevel(logging.INFO)
debug_handler.setLevel(logging.DEBUG)
stdout_handler.setLevel(logging.INFO)
sdebug_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    fmt="\x1b[1;33m[%(asctime)s \x1b[31m%(levelname)s \x1b[32m%(module)s/%(lineno)d-%(processName)s\x1b[1;33m] \x1b[0m%(message)s")
file_handler.setFormatter(formatter)
debug_handler.setFormatter(formatter)
stdout_handler.setFormatter(formatter)
sdebug_handler.setFormatter(formatter)

stdout_handler.addFilter(logging.Filter("desktopenv"))
sdebug_handler.addFilter(logging.Filter("desktopenv"))

logger.addHandler(file_handler)
logger.addHandler(debug_handler)
logger.addHandler(stdout_handler)
logger.addHandler(sdebug_handler)
#  }}} Logger Configs # 

logger = logging.getLogger("desktopenv.experiment")

# wandb config
### set your wandb api key here
# os.environ["WANDB_API_KEY"] = "48ec18fb4da7087238c6d6833eab9907565adbf3"
# wandb.login(key=os.environ.get("WANDB_API_KEY", None))


def config() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run end-to-end evaluation on the benchmark"
    )

    # environment config
    parser.add_argument("--path_to_vm", type=str,
                        default=r"C:\Users\tianbaox\Documents\Virtual Machines\Ubuntu\Ubuntu.vmx")
    parser.add_argument(
        "--headless", action="store_true", help="Run in headless machine"
    )
    parser.add_argument("--action_space", type=str, default="pyautogui", help="Action type")
    parser.add_argument(
        "--observation_type",
        choices=[
            "screenshot",
            "a11y_tree",
            "screenshot_a11y_tree",
            "som"
        ],
        default="a11y_tree",
        help="Observation type",
    )
    parser.add_argument("--screen_width", type=int, default=1920)
    parser.add_argument("--screen_height", type=int, default=1080)
    parser.add_argument("--sleep_after_execution", type=float, default=0.0)
    parser.add_argument("--max_steps", type=int, default=15)

    # agent config
    parser.add_argument("--max_trajectory_length", type=int, default=3)
    parser.add_argument("--test_config_base_dir", type=str, default="evaluation_examples")

    # lm config
    parser.add_argument("--model", type=str, default="gpt-4-0125-preview")
    parser.add_argument("--temperature", type=float, default=1.0)
    parser.add_argument("--top_p", type=float, default=0.9)
    parser.add_argument("--max_tokens", type=int, default=1500)
    parser.add_argument("--stop_token", type=str, default=None)

    # example config
    parser.add_argument("--domain", type=str, default="all")
    parser.add_argument("--test_all_meta_path", type=str, default="evaluation_examples/test_all.json")

    # logging related
    parser.add_argument("--result_dir", type=str, default="./results")
    args = parser.parse_args()

    return args


def test(
        args: argparse.Namespace,
        test_all_meta: dict
) -> None:
    scores = []
    max_steps = args.max_steps

    # log args
    logger.info("Args: %s", args)
    # set wandb project
    cfg_args = \
    {
        "path_to_vm": args.path_to_vm,
        "headless": args.headless,
        "action_space": args.action_space,
        "observation_type": args.observation_type,
        "screen_width": args.screen_width,
        "screen_height": args.screen_height,
        "sleep_after_execution": args.sleep_after_execution,
        "max_steps": args.max_steps,
        "max_trajectory_length": args.max_trajectory_length,
        "model": args.model,
        "temperature": args.temperature,
        "top_p": args.top_p,
        "max_tokens": args.max_tokens,
        "stop_token": args.stop_token,
        "result_dir": args.result_dir
    }

    agent = PromptAgent(
        model=args.model,
        max_tokens=args.max_tokens,
        action_space=args.action_space,
        observation_type=args.observation_type,
        max_trajectory_length=args.max_trajectory_length,
    )

    env = DesktopEnv(
        path_to_vm=args.path_to_vm,
        action_space=agent.action_space,
        screen_size=(args.screen_width, args.screen_height),
        headless=args.headless,
        require_a11y_tree=args.observation_type in ["a11y_tree", "screenshot_a11y_tree", "som"],
    )

    for domain in tqdm(test_all_meta, desc="Domain"):
        for example_id in tqdm(test_all_meta[domain], desc="Example", leave=False):
            # run = wandb.init(project=f"OSworld-{args.action_space}-{args.observation_type}-{args.model}", group=f"{domain}",
            #         name=f"{example_id}")
            # example setting
            config_file = os.path.join(args.test_config_base_dir, f"examples/{domain}/{example_id}.json")
            with open(config_file, "r", encoding="utf-8") as f:
                example = json.load(f)

            logger.info(f"[Domain]: {domain}")
            logger.info(f"[Example ID]: {example_id}")

            instruction = example["instruction"]

            logger.info(f"[Instruction]: {instruction}")
            # wandb each example config settings
            cfg_args["instruction"] = instruction
            cfg_args["start_time"] = datetime.datetime.now().strftime("%Y:%m:%d-%H:%M:%S")
            # run.config.update(cfg_args)

            example_result_dir = os.path.join(
                args.result_dir,
                args.action_space,
                args.observation_type,
                args.model,
                domain,
                example_id
            )
            os.makedirs(example_result_dir, exist_ok=True)
            # example start running
            try:
                lib_run_single.run_single_example(agent, env, example, max_steps, instruction, args, example_result_dir,
                                                  scores)
            except Exception as e:
                logger.error(f"Exception in {domain}/{example_id}: {e}")
                # wandb.log({"Exception": wandb.Table(data=[[f"Exception in {domain}/{example_id}: {e}"]], columns=["Error"])})
                env.controller.end_recording(os.path.join(example_result_dir, "recording.mp4"))
                with open(os.path.join(example_result_dir, "traj.jsonl"), "a") as f:
                    f.write(json.dumps({
                        "Error": f"Time limit exceeded in {domain}/{example_id}"
                    }))
                    f.write("\n")
            # wandb settings
            # os.mkdir(os.path.join(wandb.run.dir, "results/"))
            # for file in os.listdir(example_result_dir):
            #     # move file to just under the root dir
            #     os.rename(os.path.join(example_result_dir, file), os.path.join(wandb.run.dir, f"./results/{file}"))
            # wandb.finish()

    env.close()
    logger.info(f"Average score: {sum(scores) / len(scores)}")


def get_unfinished(action_space, use_model, observation_type, result_dir, total_file_json):
    target_dir = os.path.join(result_dir, action_space, observation_type, use_model)

    if not os.path.exists(target_dir):
        return total_file_json

    finished = {}
    for domain in os.listdir(target_dir):
        finished[domain] = []
        domain_path = os.path.join(target_dir, domain)
        if os.path.isdir(domain_path):
            for example_id in os.listdir(domain_path):
                if example_id == "onboard":
                    continue
                example_path = os.path.join(domain_path, example_id)
                if os.path.isdir(example_path):
                    if "result.txt" not in os.listdir(example_path):
                        # empty all files under example_id
                        for file in os.listdir(example_path):
                            os.remove(os.path.join(example_path, file))
                    else:
                        finished[domain].append(example_id)

    if not finished:
        return total_file_json

    for domain, examples in finished.items():
        if domain in total_file_json:
            total_file_json[domain] = [x for x in total_file_json[domain] if x not in examples]

    return total_file_json


def get_result(action_space, use_model, observation_type, result_dir, total_file_json):
    target_dir = os.path.join(result_dir, action_space, observation_type, use_model)
    if not os.path.exists(target_dir):
        print("New experiment, no result yet.")
        return None

    all_result = []

    for domain in os.listdir(target_dir):
        domain_path = os.path.join(target_dir, domain)
        if os.path.isdir(domain_path):
            for example_id in os.listdir(domain_path):
                example_path = os.path.join(domain_path, example_id)
                if os.path.isdir(example_path):
                    if "result.txt" in os.listdir(example_path):
                        # empty all files under example_id
                        try:
                            all_result.append(float(open(os.path.join(example_path, "result.txt"), "r").read()))
                        except:
                            all_result.append(0.0)

    if not all_result:
        print("New experiment, no result yet.")
        return None
    else:
        print("Current Success Rate:", sum(all_result) / len(all_result) * 100, "%")
        return all_result


if __name__ == '__main__':
    ####### The complete version of the list of examples #######
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    args = config()

    with open(args.test_all_meta_path, "r", encoding="utf-8") as f:
        test_all_meta = json.load(f)

    if args.domain != "all":
        test_all_meta = {args.domain: test_all_meta[args.domain]}

    test_file_list = get_unfinished(
        args.action_space,
        args.model,
        args.observation_type,
        args.result_dir,
        test_all_meta
    )
    left_info = ""
    for domain in test_file_list:
        left_info += f"{domain}: {len(test_file_list[domain])}\n"
    logger.info(f"Left tasks:\n{left_info}")

    get_result(args.action_space,
        args.model,
        args.observation_type,
        args.result_dir,
        test_all_meta
    )
    test(args, test_file_list)

```

## settings.json

```json
{
    "time_limit": "3600"
}
```

## setup_vm.py

```python
import os
import platform
import subprocess
import requests
from tqdm import tqdm
import zipfile
from time import sleep

import socket

# Define the path to the virtual machine
VM_PATH = r"Ubuntu\Ubuntu.vmx"  # change this to the path of your downloaded virtual machine
MAX_RETRY_TIMES = 10


def download_and_unzip_vm():
    # Determine the platform and CPU architecture to decide the correct VM image to download
    if platform.machine() == 'arm64':  # macOS with Apple Silicon
        url = "https://huggingface.co/datasets/xlangai/ubuntu_arm/resolve/main/Ubuntu.zip"
    elif platform.machine().lower() == 'amd64':
        url = "https://huggingface.co/datasets/xlangai/ubuntu_x86/resolve/main/Ubuntu.zip"
    else:
        raise Exception("Unsupported platform or architecture")

    # Download the virtual machine image
    print("Downloading the virtual machine image...")
    filename = "Ubuntu.zip"
    downloaded_size = 0

    while True:
        headers = {}
        if os.path.exists(filename):
            downloaded_size = os.path.getsize(filename)
            headers["Range"] = f"bytes={downloaded_size}-"

        with requests.get(url, headers=headers, stream=True) as response:
            response.raise_for_status()
            total_size = int(response.headers.get('content-length', 0))

            with open(filename, "ab") as file, tqdm(
                    desc="Progress",
                    total=total_size,
                    unit='iB',
                    unit_scale=True,
                    unit_divisor=1024,
                    initial=downloaded_size,
                    ascii=True
            ) as progress_bar:
                try:
                    for data in response.iter_content(chunk_size=1024):
                        size = file.write(data)
                        progress_bar.update(size)
                except (requests.exceptions.RequestException, IOError) as e:
                    print(f"Download error: {e}")
                    sleep(1)  # Wait for 1 second before retrying
                    print("Retrying...")
                else:
                    print("Download succeeds.")
                    break  # Download completed successfully

    # Unzip the downloaded file
    print("Unzipping the downloaded file...☕️")
    current_directory = os.getcwd()
    with zipfile.ZipFile('Ubuntu.zip', 'r') as zip_ref:
        zip_ref.extractall(current_directory)
    print("Files have been successfully extracted to the current working directory:", current_directory)


# Execute the function to download and unzip the VM
if not os.path.exists(VM_PATH):
    download_and_unzip_vm()
else:
    print(f"Virtual machine exists: {VM_PATH}")


# Determine the platform of the host machine and decide the parameter for vmrun
def get_vmrun_type():
    if platform.system() == 'Windows' or platform.system() == 'Linux':
        return '-T ws'
    elif platform.system() == 'Darwin':  # Darwin is the system name for macOS
        return '-T fusion'
    else:
        raise Exception("Unsupported operating system")


# Start the virtual machine
subprocess.run(f'vmrun {get_vmrun_type()} start "{VM_PATH}"', shell=True)
print("Starting virtual machine...")

# Get the IP address of the virtual machine
for i in range(MAX_RETRY_TIMES):
    get_vm_ip = subprocess.run(f'vmrun {get_vmrun_type()} getGuestIPAddress "{VM_PATH}" -wait', shell=True,
                               capture_output=True,
                               text=True)
    if "Error" in get_vm_ip.stdout:
        print("Retry on getting IP")
        continue
    print("Virtual machine IP address:", get_vm_ip.stdout.strip())
    break

vm_ip = get_vm_ip.stdout.strip()


def is_url_accessible(url, timeout=1):
    try:
        response = requests.head(url, timeout=timeout)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


print("--------------------------------")
url = f"http://{vm_ip}:5000/screenshot"
ckeck_url = is_url_accessible(url)
print(f"check url: {url} | is accessible: {ckeck_url}")
print("--------------------------------")


# Function used to check whether the virtual machine is ready
def download_screenshot(ip):
    url = f"http://{ip}:5000/screenshot"
    try:
        # max trey times 1, max timeout 1
        response = requests.get(url, timeout=(1, 1))
        if response.status_code == 200:
            return True
    except Exception as e:
        print(f"Error: {e}")
        print(f"Type: {type(e).__name__}")
        print(f"Error detail: {str(e)}")
        sleep(2)
    return False


# Try downloading the screenshot until successful
while not download_screenshot(vm_ip):
    print("Check whether the virtual machine is ready...")

print("Virtual machine is ready. Start to make a snapshot on the virtual machine. It would take a while...")

# Create a snapshot of the virtual machine
subprocess.run(f'vmrun {get_vmrun_type()} snapshot "{VM_PATH}" "init_state"', shell=True)
print("Snapshot created.")

```

## show_result.py

```python
import os


def get_result(action_space, use_model, observation_type, result_dir):
    target_dir = os.path.join(result_dir, action_space, observation_type, use_model)
    if not os.path.exists(target_dir):
        print("New experiment, no result yet.")
        return None

    all_result = []
    domain_result = {}
    all_result_for_analysis = {}

    for domain in os.listdir(target_dir):
        domain_path = os.path.join(target_dir, domain)
        if os.path.isdir(domain_path):
            for example_id in os.listdir(domain_path):
                example_path = os.path.join(domain_path, example_id)
                if os.path.isdir(example_path):
                    if "result.txt" in os.listdir(example_path):
                        # empty all files under example_id
                        if domain not in domain_result:
                            domain_result[domain] = []
                        result = open(os.path.join(example_path, "result.txt"), "r").read()
                        try:
                            domain_result[domain].append(float(result))
                        except:
                            domain_result[domain].append(float(bool(result)))

                        if domain not in all_result_for_analysis:
                            all_result_for_analysis[domain] = {}
                        all_result_for_analysis[domain][example_id] = domain_result[domain][-1]

                        try:
                            result = open(os.path.join(example_path, "result.txt"), "r").read()
                            try:
                                all_result.append(float(result))
                            except:
                                all_result.append(float(bool(result)))
                        except:
                            all_result.append(0.0)

    for domain in domain_result:
        print("Domain:", domain, "Runned:", len(domain_result[domain]), "Success Rate:",
              sum(domain_result[domain]) / len(domain_result[domain]) * 100, "%")

    print(">>>>>>>>>>>>>")
    print("Office", "Success Rate:", sum(
        domain_result["libreoffice_calc"] + domain_result["libreoffice_impress"] + domain_result[
            "libreoffice_writer"]) / len(
        domain_result["libreoffice_calc"] + domain_result["libreoffice_impress"] + domain_result[
            "libreoffice_writer"]) * 100, "%")
    print("Daily", "Success Rate:",
          sum(domain_result["vlc"] + domain_result["thunderbird"] + domain_result["chrome"]) / len(
              domain_result["vlc"] + domain_result["thunderbird"] + domain_result["chrome"]) * 100, "%")
    print("Professional", "Success Rate:", sum(domain_result["gimp"] + domain_result["vs_code"]) / len(
        domain_result["gimp"] + domain_result["vs_code"]) * 100, "%")

    with open(os.path.join(target_dir, "all_result.json"), "w") as f:
        f.write(str(all_result_for_analysis))

    if not all_result:
        print("New experiment, no result yet.")
        return None
    else:
        print("Runned:", len(all_result), "Current Success Rate:", sum(all_result) / len(all_result) * 100, "%")
        return all_result


if __name__ == '__main__':
    get_result("pyautogui", "gpt-4-vision-preview", "screenshot", "./results")

```

## desktop_env/README.md

```markdown

```

## desktop_env/__init__.py

```python


```

## desktop_env/controllers/python.py

```python
import json
import logging
import random
from typing import Any, Dict, Optional

import requests

from desktop_env.envs.actions import KEYBOARD_KEYS

logger = logging.getLogger("desktopenv.pycontroller")


class PythonController:
    def __init__(self, vm_ip: str, pkgs_prefix: str = "import pyautogui; import time; pyautogui.FAILSAFE = False; {command}"):
        self.vm_ip = vm_ip
        self.http_server = f"http://{vm_ip}:5000"
        self.pkgs_prefix = pkgs_prefix  # fixme: this is a hacky way to execute python commands. fix it and combine it with installation of packages

    def get_screenshot(self):
        """
        Gets a screenshot from the server. With the cursor.
        """
        response = requests.get(self.http_server + "/screenshot")
        if response.status_code == 200:
            return response.content
        else:
            logger.error("Failed to get screenshot. Status code: %d", response.status_code)
            return None

    def get_terminal_output(self):
        """ Gets the terminal output from the server. None -> no terminal output or unexpected error.
        """
        response = requests.get(self.http_server + "/terminal")
        if response.status_code == 200:
            return response.json()["output"]
        else:
            logger.error("Failed to get terminal output. Status code: %d", response.status_code)
            return None

    def get_accessibility_tree(self) -> Optional[str]:

        response: requests.Response = requests.get(self.http_server + "/accessibility")
        if response.status_code == 200:
            return response.json()["AT"]
        else:
            logger.error("Failed to get accessibility tree. Status code: %d", response.status_code)
            return None

    def get_file(self, file_path: str):
        """
        Gets a file from the server.
        """
        response = requests.post(self.http_server + "/file", data={"file_path": file_path})
        if response.status_code == 200:
            logger.info("File downloaded successfully")
            return response.content
        else:
            logger.error("Failed to get file. Status code: %d", response.status_code)
            return None

    def execute_python_command(self, command: str) -> None:
        """
        Executes a python command on the server.
        It can be used to execute the pyautogui commands, or... any other python command. who knows?
        """
        # command_list = ["python", "-c", self.pkgs_prefix.format(command=command)]
        command_list = ["python", "-c", self.pkgs_prefix.format(command=command)]
        payload = json.dumps({"command": command_list, "shell": False})
        headers = {
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(self.http_server + "/execute", headers=headers, data=payload, timeout=90)
            if response.status_code == 200:
                logger.info("Command executed successfully: %s", response.text)
            else:
                logger.error("Failed to execute command. Status code: %d", response.status_code)
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error("An error occurred while trying to execute the command: %s", e)

    def execute_action(self, action: Dict[str, Any]):
        """
        Executes an action on the server computer.
        """
        if action in ['WAIT', 'FAIL', 'DONE']:
            return

        action_type = action["action_type"]
        parameters = action["parameters"] if "parameters" in action else {}
        move_mode = random.choice(
            ["pyautogui.easeInQuad", "pyautogui.easeOutQuad", "pyautogui.easeInOutQuad", "pyautogui.easeInBounce",
             "pyautogui.easeInElastic"])
        duration = random.uniform(0.5, 1)

        if action_type == "MOVE_TO":
            if parameters == {} or None:
                self.execute_python_command("pyautogui.moveTo()")
            elif "x" in parameters and "y" in parameters:
                x = parameters["x"]
                y = parameters["y"]
                self.execute_python_command(f"pyautogui.moveTo({x}, {y}, {duration}, {move_mode})")
            else:
                raise Exception(f"Unknown parameters: {parameters}")

        elif action_type == "CLICK":
            if parameters == {} or None:
                self.execute_python_command("pyautogui.click()")
            elif "button" in parameters and "x" in parameters and "y" in parameters:
                button = parameters["button"]
                x = parameters["x"]
                y = parameters["y"]
                if "num_clicks" in parameters:
                    num_clicks = parameters["num_clicks"]
                    self.execute_python_command(
                        f"pyautogui.click(button='{button}', x={x}, y={y}, clicks={num_clicks})")
                else:
                    self.execute_python_command(f"pyautogui.click(button='{button}', x={x}, y={y})")
            elif "button" in parameters and "x" not in parameters and "y" not in parameters:
                button = parameters["button"]
                if "num_clicks" in parameters:
                    num_clicks = parameters["num_clicks"]
                    self.execute_python_command(f"pyautogui.click(button='{button}', clicks={num_clicks})")
                else:
                    self.execute_python_command(f"pyautogui.click(button='{button}')")
            elif "button" not in parameters and "x" in parameters and "y" in parameters:
                x = parameters["x"]
                y = parameters["y"]
                if "num_clicks" in parameters:
                    num_clicks = parameters["num_clicks"]
                    self.execute_python_command(f"pyautogui.click(x={x}, y={y}, clicks={num_clicks})")
                else:
                    self.execute_python_command(f"pyautogui.click(x={x}, y={y})")
            else:
                raise Exception(f"Unknown parameters: {parameters}")

        elif action_type == "MOUSE_DOWN":
            if parameters == {} or None:
                self.execute_python_command("pyautogui.mouseDown()")
            elif "button" in parameters:
                button = parameters["button"]
                self.execute_python_command(f"pyautogui.mouseDown(button='{button}')")
            else:
                raise Exception(f"Unknown parameters: {parameters}")

        elif action_type == "MOUSE_UP":
            if parameters == {} or None:
                self.execute_python_command("pyautogui.mouseUp()")
            elif "button" in parameters:
                button = parameters["button"]
                self.execute_python_command(f"pyautogui.mouseUp(button='{button}')")
            else:
                raise Exception(f"Unknown parameters: {parameters}")

        elif action_type == "RIGHT_CLICK":
            if parameters == {} or None:
                self.execute_python_command("pyautogui.rightClick()")
            elif "x" in parameters and "y" in parameters:
                x = parameters["x"]
                y = parameters["y"]
                self.execute_python_command(f"pyautogui.rightClick(x={x}, y={y})")
            else:
                raise Exception(f"Unknown parameters: {parameters}")

        elif action_type == "DOUBLE_CLICK":
            if parameters == {} or None:
                self.execute_python_command("pyautogui.doubleClick()")
            elif "x" in parameters and "y" in parameters:
                x = parameters["x"]
                y = parameters["y"]
                self.execute_python_command(f"pyautogui.doubleClick(x={x}, y={y})")
            else:
                raise Exception(f"Unknown parameters: {parameters}")

        elif action_type == "DRAG_TO":
            if "x" in parameters and "y" in parameters:
                x = parameters["x"]
                y = parameters["y"]
                self.execute_python_command(
                    f"pyautogui.dragTo({x}, {y}, duration=1.0, button='left', mouseDownUp=True)")

        elif action_type == "SCROLL":
            # todo: check if it is related to the operating system, as https://github.com/TheDuckAI/DuckTrack/blob/main/ducktrack/playback.py pointed out
            if "dx" in parameters and "dy" in parameters:
                dx = parameters["dx"]
                dy = parameters["dy"]
                self.execute_python_command(f"pyautogui.hscroll({dx})")
                self.execute_python_command(f"pyautogui.vscroll({dy})")
            elif "dx" in parameters and "dy" not in parameters:
                dx = parameters["dx"]
                self.execute_python_command(f"pyautogui.hscroll({dx})")
            elif "dx" not in parameters and "dy" in parameters:
                dy = parameters["dy"]
                self.execute_python_command(f"pyautogui.vscroll({dy})")
            else:
                raise Exception(f"Unknown parameters: {parameters}")

        elif action_type == "TYPING":
            if "text" not in parameters:
                raise Exception(f"Unknown parameters: {parameters}")
            # deal with special ' and \ characters
            # text = parameters["text"].replace("\\", "\\\\").replace("'", "\\'")
            # self.execute_python_command(f"pyautogui.typewrite('{text}')")
            text = parameters["text"]
            self.execute_python_command("pyautogui.typewrite({:})".format(repr(text)))

        elif action_type == "PRESS":
            if "key" not in parameters:
                raise Exception(f"Unknown parameters: {parameters}")
            key = parameters["key"]
            if key.lower() not in KEYBOARD_KEYS:
                raise Exception(f"Key must be one of {KEYBOARD_KEYS}")
            self.execute_python_command(f"pyautogui.press('{key}')")

        elif action_type == "KEY_DOWN":
            if "key" not in parameters:
                raise Exception(f"Unknown parameters: {parameters}")
            key = parameters["key"]
            if key.lower() not in KEYBOARD_KEYS:
                raise Exception(f"Key must be one of {KEYBOARD_KEYS}")
            self.execute_python_command(f"pyautogui.keyDown('{key}')")

        elif action_type == "KEY_UP":
            if "key" not in parameters:
                raise Exception(f"Unknown parameters: {parameters}")
            key = parameters["key"]
            if key.lower() not in KEYBOARD_KEYS:
                raise Exception(f"Key must be one of {KEYBOARD_KEYS}")
            self.execute_python_command(f"pyautogui.keyUp('{key}')")

        elif action_type == "HOTKEY":
            if "keys" not in parameters:
                raise Exception(f"Unknown parameters: {parameters}")
            keys = parameters["keys"]
            if not isinstance(keys, list):
                raise Exception("Keys must be a list of keys")
            for key in keys:
                if key.lower() not in KEYBOARD_KEYS:
                    raise Exception(f"Key must be one of {KEYBOARD_KEYS}")

            keys_para_rep = "', '".join(keys)
            self.execute_python_command(f"pyautogui.hotkey('{keys_para_rep}')")

        elif action_type in ['WAIT', 'FAIL', 'DONE']:
            pass

        else:
            raise Exception(f"Unknown action type: {action_type}")

    # Record video
    def start_recording(self):
        """
        Starts recording the screen.
        """
        response = requests.post(self.http_server + "/start_recording")
        if response.status_code == 200:
            logger.info("Recording started successfully")
        else:
            logger.error("Failed to start recording. Status code: %d", response.status_code)

    def end_recording(self, dest: str):
        """
        Ends recording the screen.
        """
        try:
            response = requests.post(self.http_server + "/end_recording")
            if response.status_code == 200:
                logger.info("Recording stopped successfully")
                with open(dest, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
            else:
                logger.error("Failed to stop recording. Status code: %d", response.status_code)
                return None
        except Exception as e:
            logger.error("An error occurred while trying to download the recording: %s", e)

    # Additional info
    def get_vm_platform(self):
        """
        Gets the size of the vm screen.
        """
        return self.execute_python_command("import platform; print(platform.system())")['output'].strip()

    def get_vm_screen_size(self):
        """
        Gets the size of the vm screen.
        """
        response = requests.post(self.http_server + "/screen_size")
        if response.status_code == 200:
            return response.json()
        else:
            logger.error("Failed to get screen size. Status code: %d", response.status_code)
            return None

    def get_vm_window_size(self, app_class_name: str):
        """
        Gets the size of the vm app window.
        """
        response = requests.post(self.http_server + "/window_size", data={"app_class_name": app_class_name})
        if response.status_code == 200:
            return response.json()
        else:
            logger.error("Failed to get window size. Status code: %d", response.status_code)
            return None

    def get_vm_wallpaper(self):
        """
        Gets the wallpaper of the vm.
        """
        response = requests.post(self.http_server + "/wallpaper")
        if response.status_code == 200:
            logger.info("Wallpaper downloaded successfully")
            return response.content
        else:
            logger.error("Failed to get wallpaper. Status code: %d", response.status_code)
            return None

    def get_vm_desktop_path(self):
        """
        Gets the desktop path of the vm.
        """
        response = requests.post(self.http_server + "/desktop_path")
        if response.status_code == 200:
            logger.info("Desktop path downloaded successfully")
            return response.json()["desktop_path"]
        else:
            logger.error("Failed to get desktop path. Status code: %d", response.status_code)
            return None

    def get_vm_directory_tree(self, path):
        """
        Gets the directory tree of the vm.
        """
        payload = json.dumps({"path": path})
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(self.http_server + "/list_directory", headers=headers, data=payload)
        if response.status_code == 200:
            logger.info("Directory tree downloaded successfully")
            return response.json()["directory_tree"]
        else:
            logger.error("Failed to get directory tree. Status code: %d", response.status_code)
            return None

```

## desktop_env/controllers/setup.py

```python
import json
import logging
import os
import os.path
import sqlite3
import tempfile
import time
import traceback
import uuid
from datetime import datetime, timedelta
from typing import Any, Union, Optional
from typing import Dict, List

import shutil
import requests
from playwright.sync_api import sync_playwright, TimeoutError
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive, GoogleDriveFile, GoogleDriveFileList
from requests_toolbelt.multipart.encoder import MultipartEncoder

from desktop_env.controllers.python import PythonController
from desktop_env.evaluators.metrics.utils import compare_urls

logger = logging.getLogger("desktopenv.setup")

FILE_PATH = os.path.dirname(os.path.abspath(__file__))

class SetupController:
    def __init__(self, vm_ip: str, cache_dir: str):
        self.vm_ip: str = vm_ip
        self.http_server: str = f"http://{vm_ip}:5000"
        self.http_server_setup_root: str = f"http://{vm_ip}:5000/setup"
        self.cache_dir: str = cache_dir

    def reset_cache_dir(self, cache_dir: str):
        self.cache_dir = cache_dir

    def setup(self, config: List[Dict[str, Any]]):
        """
        Args:
            config (List[Dict[str, Any]]): list of dict like {str: Any}. each
              config dict has the structure like
                {
                    "type": str, corresponding to the `_{:}_setup` methods of
                      this class
                    "parameters": dick like {str, Any} providing the keyword
                      parameters
                }
        """

        for cfg in config:
            config_type: str = cfg["type"]
            parameters: Dict[str, Any] = cfg["parameters"]

            # Assumes all the setup the functions should follow this name
            # protocol
            setup_function: str = "_{:}_setup".format(config_type)
            assert hasattr(self, setup_function), f'Setup controller cannot find init function {setup_function}'
            getattr(self, setup_function)(**parameters)

            logger.info("SETUP: %s(%s)", setup_function, str(parameters))

        # self._download_setup(config)
        # self._change_wallpaper(config)
        # self._tidy_desktop(config) todo: implement this
        # self._open_setup(config)
        # can add other setup steps

    # ZDY_COMMENT: merged with launch
    # def _command_setup(self, command: str):
    # """
    # Directly send a command into the virtual machine os for setting up.
    # """
    # payload = json.dumps({"command": command})
    # headers = {
    # 'Content-Type': 'application/json'
    # }
    # timeout = 5
    # timout_whitelist = ["vlc"]
    #
    # try:
    #
    # response = requests.post(self.http_server + "/execute", headers=headers, data=payload, timeout=timeout)
    # if response.status_code == 200:
    # print("Command executed successfully:", response.text)
    # else:
    # print("Failed to execute command. Status code:", response.status_code)
    # except requests.exceptions.Timeout as e:
    # if command in timout_whitelist:
    # print("Command executed successfully:", command)
    # else:
    # print("An error occurred while trying to execute the command:", e)
    # except requests.exceptions.RequestException as e:
    # print("An error occurred while trying to execute the command:", e)

    def _download_setup(self, files: List[Dict[str, str]]):
        """
        Args:
            files (List[Dict[str, str]]): files to download. lisf of dict like
              {
                "url": str, the url to download
                "path": str, the path on the VM to store the downloaded file
              }
        """

        # if not config:
        # return
        # if not 'download' in config:
        # return
        # for url, path in config['download']:
        for f in files:
            url: str = f["url"]
            path: str = f["path"]
            cache_path: str = os.path.join(self.cache_dir, "{:}_{:}".format(
                uuid.uuid5(uuid.NAMESPACE_URL, url),
                os.path.basename(path)))
            if not url or not path:
                raise Exception(f"Setup Download - Invalid URL ({url}) or path ({path}).")

            if not os.path.exists(cache_path):
                max_retries = 3
                downloaded = False
                e = None
                for i in range(max_retries):
                    try:
                        response = requests.get(url, stream=True)
                        response.raise_for_status()

                        with open(cache_path, 'wb') as f:
                            for chunk in response.iter_content(chunk_size=8192):
                                if chunk:
                                    f.write(chunk)
                        logger.info("File downloaded successfully")
                        downloaded = True
                        break

                    except requests.RequestException as e:
                        logger.error(
                            f"Failed to download {url} caused by {e}. Retrying... ({max_retries - i - 1} attempts left)")
                if not downloaded:
                    raise requests.RequestException(f"Failed to download {url}. No retries left. Error: {e}")

            # payload = json.dumps({"url": url, "path": path})
            # headers = {
            # 'Content-Type': 'application/json'
            # }

            form = MultipartEncoder({
                "file_path": path,
                "file_data": (os.path.basename(path), open(cache_path, "rb"))
            })
            headers = {"Content-Type": form.content_type}
            logger.debug(form.content_type)

            # send request to server to upload file
            try:
                logger.debug("REQUEST ADDRESS: %s", self.http_server + "/setup" + "/upload")
                response = requests.post(self.http_server + "/setup" + "/upload", headers=headers, data=form)
                if response.status_code == 200:
                    logger.info("Command executed successfully: %s", response.text)
                else:
                    logger.error("Failed to upload file. Status code: %s", response.text)
            except requests.exceptions.RequestException as e:
                logger.error("An error occurred while trying to send the request: %s", e)

    def _change_wallpaper_setup(self, path: str):
        # if not config:
        # return
        # if not 'wallpaper' in config:
        # return

        # path = config['wallpaper']
        if not path:
            raise Exception(f"Setup Wallpaper - Invalid path ({path}).")

        payload = json.dumps({"path": path})
        headers = {
            'Content-Type': 'application/json'
        }

        # send request to server to change wallpaper
        try:
            response = requests.post(self.http_server + "/setup" + "/change_wallpaper", headers=headers, data=payload)
            if response.status_code == 200:
                logger.info("Command executed successfully: %s", response.text)
            else:
                logger.error("Failed to change wallpaper. Status code: %s", response.text)
        except requests.exceptions.RequestException as e:
            logger.error("An error occurred while trying to send the request: %s", e)

    def _tidy_desktop_setup(self, **config):
        raise NotImplementedError()

    def _open_setup(self, path: str):
        # if not config:
        # return
        # if not 'open' in config:
        # return
        # for path in config['open']:
        if not path:
            raise Exception(f"Setup Open - Invalid path ({path}).")

        payload = json.dumps({"path": path})
        headers = {
            'Content-Type': 'application/json'
        }

        # send request to server to open file
        try:
            response = requests.post(self.http_server + "/setup" + "/open_file", headers=headers, data=payload)
            if response.status_code == 200:
                logger.info("Command executed successfully: %s", response.text)
            else:
                logger.error("Failed to open file. Status code: %s", response.text)
        except requests.exceptions.RequestException as e:
            logger.error("An error occurred while trying to send the request: %s", e)

    def _launch_setup(self, command: Union[str, List[str]], shell: bool = False):
        if not command:
            raise Exception("Empty command to launch.")

        if not shell and isinstance(command, str) and len(command.split()) > 1:
            logger.warning("Command should be a list of strings. Now it is a string. Will split it by space.")
            command = command.split()

        payload = json.dumps({"command": command, "shell": shell})
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(self.http_server + "/setup" + "/launch", headers=headers, data=payload)
            if response.status_code == 200:
                logger.info("Command executed successfully: %s", response.text)
            else:
                logger.error("Failed to launch application. Status code: %s", response.text)
        except requests.exceptions.RequestException as e:
            logger.error("An error occurred while trying to send the request: %s", e)

    def _execute_setup(
            self,
            command: List[str],
            stdout: str = "",
            stderr: str = "",
            shell: bool = False,
            until: Optional[Dict[str, Any]] = None
    ):
        if not command:
            raise Exception("Empty comman to launch.")

        until: Dict[str, Any] = until or {}
        terminates: bool = False
        nb_failings = 0

        payload = json.dumps({"command": command, "shell": shell})
        headers = {"Content-Type": "application/json"}

        while not terminates:
            try:
                response = requests.post(self.http_server + "/setup" + "/execute", headers=headers, data=payload)
                if response.status_code == 200:
                    results: Dict[str, str] = response.json()
                    if stdout:
                        with open(os.path.join(self.cache_dir, stdout), "w") as f:
                            f.write(results["output"])
                    if stderr:
                        with open(os.path.join(self.cache_dir, stderr), "w") as f:
                            f.write(results["error"])
                    logger.info("Command executed successfully: %s -> %s"
                                , " ".join(command) if isinstance(command, list) else command
                                , response.text
                                )
                else:
                    logger.error("Failed to launch application. Status code: %s", response.text)
                    results = None
                    nb_failings += 1
            except requests.exceptions.RequestException as e:
                logger.error("An error occurred while trying to send the request: %s", e)
                traceback.print_exc()

                results = None
                nb_failings += 1

            if len(until) == 0:
                terminates = True
            elif results is not None:
                terminates = "returncode" in until and results["returncode"] == until["returncode"] \
                             or "stdout" in until and until["stdout"] in results["output"] \
                             or "stderr" in until and until["stderr"] in results["error"]
            terminates = terminates or nb_failings >= 5
            if not terminates:
                time.sleep(0.3)

    def _command_setup(self, command: List[str], **kwargs):
        self._execute_setup(command, **kwargs)

    def _sleep_setup(self, seconds: float):
        time.sleep(seconds)

    def _act_setup(self, action_seq: List[Union[Dict[str, Any], str]]):
        # TODO
        raise NotImplementedError()

    def _replay_setup(self, trajectory: str):
        """
        Args:
            trajectory (str): path to the replay trajectory file
        """

        # TODO
        raise NotImplementedError()

    def _activate_window_setup(self, window_name: str, strict: bool = False, by_class: bool = False):
        if not window_name:
            raise Exception(f"Setup Open - Invalid path ({window_name}).")

        payload = json.dumps({"window_name": window_name, "strict": strict, "by_class": by_class})
        headers = {
            'Content-Type': 'application/json'
        }

        # send request to server to open file
        try:
            response = requests.post(self.http_server + "/setup" + "/activate_window", headers=headers, data=payload)
            if response.status_code == 200:
                logger.info("Command executed successfully: %s", response.text)
            else:
                logger.error(f"Failed to activate window {window_name}. Status code: %s", response.text)
        except requests.exceptions.RequestException as e:
            logger.error("An error occurred while trying to send the request: %s", e)

    def _close_window_setup(self, window_name: str, strict: bool = False, by_class: bool = False):
        if not window_name:
            raise Exception(f"Setup Open - Invalid path ({window_name}).")

        payload = json.dumps({"window_name": window_name, "strict": strict, "by_class": by_class})
        headers = {
            'Content-Type': 'application/json'
        }

        # send request to server to open file
        try:
            response = requests.post(self.http_server + "/setup" + "/close_window", headers=headers, data=payload)
            if response.status_code == 200:
                logger.info("Command executed successfully: %s", response.text)
            else:
                logger.error(f"Failed to close window {window_name}. Status code: %s", response.text)
        except requests.exceptions.RequestException as e:
            logger.error("An error occurred while trying to send the request: %s", e)

    # Chrome setup
    def _chrome_open_tabs_setup(self, urls_to_open: List[str]):
        host = self.vm_ip
        port = 9222  # fixme: this port is hard-coded, need to be changed from config file

        remote_debugging_url = f"http://{host}:{port}"
        logger.info("Connect to Chrome @: %s", remote_debugging_url)
        logger.debug("PLAYWRIGHT ENV: %s", repr(os.environ))
        for attempt in range(15):
            if attempt > 0:
                time.sleep(5)

            browser = None
            with sync_playwright() as p:
                try:
                    browser = p.chromium.connect_over_cdp(remote_debugging_url)
                    # break
                except Exception as e:
                    if attempt < 14:
                        logger.error(f"Attempt {attempt + 1}: Failed to connect, retrying. Error: {e}")
                        # time.sleep(10)
                        continue
                    else:
                        logger.error(f"Failed to connect after multiple attempts: {e}")
                        raise e

                if not browser:
                    return

                logger.info("Opening %s...", urls_to_open)
                for i, url in enumerate(urls_to_open):
                    # Use the first context (which should be the only one if using default profile)
                    if i == 0:
                        context = browser.contexts[0]

                    page = context.new_page()  # Create a new page (tab) within the existing context
                    try:
                        page.goto(url, timeout=60000)
                    except:
                        logger.warning("Opening %s exceeds time limit", url)  # only for human test
                    logger.info(f"Opened tab {i + 1}: {url}")

                    if i == 0:
                        # clear the default tab
                        default_page = context.pages[0]
                        default_page.close()

                # Do not close the context or browser; they will remain open after script ends
                return browser, context

    def _chrome_close_tabs_setup(self, urls_to_close: List[str]):
        time.sleep(5)  # Wait for Chrome to finish launching

        host = self.vm_ip
        port = 9222  # fixme: this port is hard-coded, need to be changed from config file

        remote_debugging_url = f"http://{host}:{port}"
        with sync_playwright() as p:
            browser = None
            for attempt in range(15):
                try:
                    browser = p.chromium.connect_over_cdp(remote_debugging_url)
                    break
                except Exception as e:
                    if attempt < 14:
                        logger.error(f"Attempt {attempt + 1}: Failed to connect, retrying. Error: {e}")
                        time.sleep(5)
                    else:
                        logger.error(f"Failed to connect after multiple attempts: {e}")
                        raise e

            if not browser:
                return

            for i, url in enumerate(urls_to_close):
                # Use the first context (which should be the only one if using default profile)
                if i == 0:
                    context = browser.contexts[0]

                for page in context.pages:

                    # if two urls are the same, close the tab
                    if compare_urls(page.url, url):
                        context.pages.pop(context.pages.index(page))
                        page.close()
                        logger.info(f"Closed tab {i + 1}: {url}")
                        break

            # Do not close the context or browser; they will remain open after script ends
            return browser, context

    # google drive setup
    def _googledrive_setup(self, **config):
        """ Clean google drive space (eliminate the impact of previous experiments to reset the environment)
        @args:
            config(Dict[str, Any]): contain keys
                settings_file(str): path to google drive settings file, which will be loaded by pydrive.auth.GoogleAuth()
                operation(List[str]): each operation is chosen from ['delete', 'upload']
                args(List[Dict[str, Any]]): parameters for each operation
            different args dict for different operations:
                for delete:
                    query(str): query pattern string to search files or folder in google drive to delete, please refer to
                        https://developers.google.com/drive/api/guides/search-files?hl=en about how to write query string.
                    trash(bool): whether to delete files permanently or move to trash. By default, trash=false, completely delete it.
                for mkdirs:
                    path(List[str]): the path in the google drive to create folder
                for upload:
                    path(str): remote url to download file
                    dest(List[str]): the path in the google drive to store the downloaded file
        """
        settings_file = config.get('settings_file', 'evaluation_examples/settings/googledrive/settings.yml')
        gauth = GoogleAuth(settings_file=settings_file)
        drive = GoogleDrive(gauth)

        def mkdir_in_googledrive(paths: List[str]):
            paths = [paths] if type(paths) != list else paths
            parent_id = 'root'
            for p in paths:
                q = f'"{parent_id}" in parents and title = "{p}" and mimeType = "application/vnd.google-apps.folder" and trashed = false'
                folder = drive.ListFile({'q': q}).GetList()
                if len(folder) == 0:  # not exists, create it
                    parents = {} if parent_id == 'root' else {'parents': [{'id': parent_id}]}
                    file = drive.CreateFile({'title': p, 'mimeType': 'application/vnd.google-apps.folder', **parents})
                    file.Upload()
                    parent_id = file['id']
                else:
                    parent_id = folder[0]['id']
            return parent_id

        for oid, operation in enumerate(config['operation']):
            if operation == 'delete':  # delete a specific file
                # query pattern string, by default, remove all files/folders not in the trash to the trash
                params = config['args'][oid]
                q = params.get('query', '')
                trash = params.get('trash', False)
                q_file = f"( {q} ) and mimeType != 'application/vnd.google-apps.folder'" if q.strip() else "mimeType != 'application/vnd.google-apps.folder'"
                filelist: GoogleDriveFileList = drive.ListFile({'q': q_file}).GetList()
                q_folder = f"( {q} ) and mimeType = 'application/vnd.google-apps.folder'" if q.strip() else "mimeType = 'application/vnd.google-apps.folder'"
                folderlist: GoogleDriveFileList = drive.ListFile({'q': q_folder}).GetList()
                for file in filelist:  # first delete file, then folder
                    file: GoogleDriveFile
                    if trash:
                        file.Trash()
                    else:
                        file.Delete()
                for folder in folderlist:
                    folder: GoogleDriveFile
                    # note that, if a folder is trashed/deleted, all files and folders in it will be trashed/deleted
                    if trash:
                        folder.Trash()
                    else:
                        folder.Delete()
            elif operation == 'mkdirs':
                params = config['args'][oid]
                mkdir_in_googledrive(params['path'])
            elif operation == 'upload':
                params = config['args'][oid]
                url = params['url']
                with tempfile.NamedTemporaryFile(mode='wb', delete=False) as tmpf:
                    response = requests.get(url, stream=True)
                    response.raise_for_status()
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            tmpf.write(chunk)
                    tmpf.close()
                    paths = [params['path']] if params['path'] != list else params['path']
                    parent_id = mkdir_in_googledrive(paths[:-1])
                    parents = {} if parent_id == 'root' else {'parents': [{'id': parent_id}]}
                    file = drive.CreateFile({'title': paths[-1], **parents})
                    file.SetContentFile(tmpf.name)
                    file.Upload()
                return
            else:
                raise ValueError('[ERROR]: not implemented clean type!')

    def _login_setup(self, **config):
        """ Login to a website with account and password information.
        @args:
            config(Dict[str, Any]): contain keys
                settings_file(str): path to the settings file
                platform(str): platform to login, implemented platforms include:
                    googledrive: https://drive.google.com/drive/my-drive

        """
        host = self.vm_ip
        port = 9222  # fixme: this port is hard-coded, need to be changed from config file

        remote_debugging_url = f"http://{host}:{port}"
        with sync_playwright() as p:
            browser = None
            for attempt in range(15):
                try:
                    browser = p.chromium.connect_over_cdp(remote_debugging_url)
                    break
                except Exception as e:
                    if attempt < 14:
                        logger.error(f"Attempt {attempt + 1}: Failed to connect, retrying. Error: {e}")
                        time.sleep(5)
                    else:
                        logger.error(f"Failed to connect after multiple attempts: {e}")
                        raise e
            if not browser:
                return

            context = browser.contexts[0]
            platform = config['platform']

            if platform == 'googledrive':
                url = 'https://drive.google.com/drive/my-drive'
                page = context.new_page()  # Create a new page (tab) within the existing context
                try:
                    page.goto(url, timeout=60000)
                except:
                    logger.warning("Opening %s exceeds time limit", url) # only for human test
                logger.info(f"Opened new page: {url}")
                settings = json.load(open(config['settings_file']))
                email, password = settings['email'], settings['password']

                try:
                    page.wait_for_selector('input[type="email"]', state="visible", timeout=3000)
                    page.fill('input[type="email"]', email)
                    page.click('#identifierNext > div > button')
                    page.wait_for_selector('input[type="password"]', state="visible", timeout=5000)
                    page.fill('input[type="password"]', password)
                    page.click('#passwordNext > div > button')
                    page.wait_for_load_state('load', timeout=5000)
                except TimeoutError:
                    logger.info('[ERROR]: timeout when waiting for google drive login page to load!')
                    return

            else:
                raise NotImplementedError

            return browser, context

    def _update_browse_history_setup(self, **config):
        db_path = os.path.join("desktop_env", "assets", "history_empty.sqlite")

        # copy a new history file in the tmp folder
        cache_path = os.path.join(self.cache_dir, "history_new.sqlite")
        shutil.copyfile(db_path, cache_path)
        db_path = cache_path

        history = config['history']

        for history_item in history:
            url = history_item['url']
            title = history_item['title']
            visit_time = datetime.now() - timedelta(seconds=history_item['visit_time_from_now_in_seconds'])

            # Chrome use ms from 1601-01-01 as timestamp
            epoch_start = datetime(1601, 1, 1)
            chrome_timestamp = int((visit_time - epoch_start).total_seconds() * 1000000)

            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            cursor.execute('''
                   INSERT INTO urls (url, title, visit_count, typed_count, last_visit_time, hidden)
                   VALUES (?, ?, ?, ?, ?, ?)
               ''', (url, title, 1, 0, chrome_timestamp, 0))

            url_id = cursor.lastrowid

            cursor.execute('''
                   INSERT INTO visits (url, visit_time, from_visit, transition, segment_id, visit_duration)
                   VALUES (?, ?, ?, ?, ?, ?)
               ''', (url_id, chrome_timestamp, 0, 805306368, 0, 0))

            conn.commit()
            conn.close()

        logger.info('Fake browsing history added successfully.')

        controller = PythonController(self.vm_ip)

        # get the path of the history file according to the platform
        os_type = controller.get_vm_platform()

        if os_type == 'Windows':
            chrome_history_path = controller.execute_python_command(
                """import os; print(os.path.join(os.getenv('USERPROFILE'), "AppData", "Local", "Google", "Chrome", "User Data", "Default", "History"))""")[
                'output'].strip()
        elif os_type == 'Darwin':
            chrome_history_path = controller.execute_python_command(
                """import os; print(os.path.join(os.getenv('HOME'), "Library", "Application Support", "Google", "Chrome", "Default", "History"))""")[
                'output'].strip()
        elif os_type == 'Linux':
            chrome_history_path = controller.execute_python_command(
                "import os; print(os.path.join(os.getenv('HOME'), '.config', 'google-chrome', 'Default', 'History'))")[
                'output'].strip()
        else:
            raise Exception('Unsupported operating system')

        form = MultipartEncoder({
            "file_path": chrome_history_path,
            "file_data": (os.path.basename(chrome_history_path), open(db_path, "rb"))
        })
        headers = {"Content-Type": form.content_type}
        logger.debug(form.content_type)

        # send request to server to upload file
        try:
            logger.debug("REQUEST ADDRESS: %s", self.http_server + "/setup" + "/upload")
            response = requests.post(self.http_server + "/setup" + "/upload", headers=headers, data=form)
            if response.status_code == 200:
                logger.info("Command executed successfully: %s", response.text)
            else:
                logger.error("Failed to upload file. Status code: %s", response.text)
        except requests.exceptions.RequestException as e:
            logger.error("An error occurred while trying to send the request: %s", e)

        self._execute_setup(["sudo chown -R user:user /home/user/.config/google-chrome/Default/History"], shell=True)

```

## desktop_env/controllers/__init__.py

```python

```

## desktop_env/envs/actions.py

```python
X_MAX = 1920  # TODO: get the screen resolution
Y_MAX = 1080

KEYBOARD_KEYS = ['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', 'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace', 'browserback', 'browserfavorites', 'browserforward', 'browserhome', 'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear', 'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete', 'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20', 'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja', 'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail', 'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack', 'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6', 'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn', 'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn', 'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator', 'shift', 'shiftleft', 'shiftright', 'sleep', 'stop', 'subtract', 'tab', 'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen', 'command', 'option', 'optionleft', 'optionright']

ACTION_SPACE = [
    {
        "action_type": "MOVE_TO",
        "note": "move the cursor to the specified position",
        "parameters": {
            "x": {
                "type": float,
                "range": [0, X_MAX],
                "optional": False,
            },
            "y": {
                "type": float,
                "range": [0, Y_MAX],
                "optional": False,
            }
        }
    },
    {
        "action_type": "CLICK",
        "note": "click the left button if the button not specified, otherwise click the specified button; click at the current position if x and y are not specified, otherwise click at the specified position",
        "parameters": {
            "button": {
                "type": str,
                "range": ["left", "right", "middle"],
                "optional": True,
            },
            "x": {
                "type": float,
                "range": [0, X_MAX],
                "optional": True,
            },
            "y": {
                "type": float,
                "range": [0, Y_MAX],
                "optional": True,
            },
            "num_clicks": {
                "type": int,
                "range": [1, 2, 3],
                "optional": True,
            },
        }
    },
    {
        "action_type": "MOUSE_DOWN",
        "note": "press the left button if the button not specified, otherwise press the specified button",
        "parameters": {
            "button": {
                "type": str,
                "range": ["left", "right", "middle"],
                "optional": True,
            }
        }
    },
    {
        "action_type": "MOUSE_UP",
        "note": "release the left button if the button not specified, otherwise release the specified button",
        "parameters": {
            "button": {
                "type": str,
                "range": ["left", "right", "middle"],
                "optional": True,
            }
        }
    },
    {
        "action_type": "RIGHT_CLICK",
        "note": "right click at the current position if x and y are not specified, otherwise right click at the specified position",
        "parameters": {
            "x": {
                "type": float,
                "range": [0, X_MAX],
                "optional": True,
            },
            "y": {
                "type": float,
                "range": [0, Y_MAX],
                "optional": True,
            }
        }
    },
    {
        "action_type": "DOUBLE_CLICK",
        "note": "double click at the current position if x and y are not specified, otherwise double click at the specified position",
        "parameters": {
            "x": {
                "type": float,
                "range": [0, X_MAX],
                "optional": True,
            },
            "y": {
                "type": float,
                "range": [0, Y_MAX],
                "optional": True,
            }
        }
    },
    {
        "action_type": "DRAG_TO",
        "note": "drag the cursor to the specified position with the left button pressed",
        "parameters": {
            "x": {
                "type": float,
                "range": [0, X_MAX],
                "optional": False,
            },
            "y": {
                "type": float,
                "range": [0, Y_MAX],
                "optional": False,
            }
        }
    },
    {
        "action_type": "SCROLL",
        "note": "scroll the mouse wheel up or down",
        "parameters": {
            "dx": {
                "type": int,
                "range": None,
                "optional": False,
            },
            "dy": {
                "type": int,
                "range": None,
                "optional": False,
            }
        }
    },
    {
        "action_type": "TYPING",
        "note": "type the specified text",
        "parameters": {
            "text": {
                "type": str,
                "range": None,
                "optional": False,
            }
        }
    },
    {
        "action_type": "PRESS",
        "note": "press the specified key and release it",
        "parameters": {
            "key": {
                "type": str,
                "range": KEYBOARD_KEYS,
                "optional": False,
            }
        }
    },
    {
        "action_type": "KEY_DOWN",
        "note": "press the specified key",
        "parameters": {
            "key": {
                "type": str,
                "range": KEYBOARD_KEYS,
                "optional": False,
            }
        }
    },
    {
        "action_type": "KEY_UP",
        "note": "release the specified key",
        "parameters": {
            "key": {
                "type": str,
                "range": KEYBOARD_KEYS,
                "optional": False,
            }
        }
    },
    {
        "action_type": "HOTKEY",
        "note": "press the specified key combination",
        "parameters": {
            "keys": {
                "type": list,
                "range": [KEYBOARD_KEYS],
                "optional": False,
            }
        }
    },
    ############################################################################################################
    {
        "action_type": "WAIT",
        "note": "wait until the next action",
    },
    {
        "action_type": "FAIL",
        "note": "decide the task can not be performed",
    },
    {
        "action_type": "DONE",
        "note": "decide the task is done",
    }
]

```

## desktop_env/envs/desktop_env.py

```python
from __future__ import annotations

import logging
import os
import subprocess
import tempfile
import time
from typing import Callable, Any, Optional, Tuple
# import uuid
# import platform
from typing import List, Dict, Union

import gymnasium as gym

from desktop_env.controllers.python import PythonController
from desktop_env.controllers.setup import SetupController
# from desktop_env.evaluators import eval_funcs
from desktop_env.evaluators import metrics, getters

# import requests

logger = logging.getLogger("desktopenv.env")

Metric = Callable[[Any, Any], float]
Getter = Callable[[gym.Env, Dict[str, Any]], Any]


def _execute_command(command: List[str]) -> None:
    def _is_contained_in(a, b):
        for v in set(a):
            if a.count(v) > b.count(v):
                return False
        return True

    # Specially handled for the `vmrun` command in Windows
    if _is_contained_in(["vmrun", "-T", "ws", "start"], command):
        p = subprocess.Popen(command)
        p.wait()
    else:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60, text=True,
                                encoding="utf-8")
        if result.returncode != 0:
            raise Exception("\033[91m" + result.stdout + result.stderr + "\033[0m")
        return result.stdout


class DesktopEnv(gym.Env):
    """
    DesktopEnv with OpenAI Gym interface.
    Fixme: refactor the logic when implementing the multi-process version
    """

    def __init__(
            self,
            path_to_vm: str,
            snapshot_name: str = "init_state",
            action_space: str = "computer_13",
            tmp_dir: str = "tmp",
            cache_dir: str = "cache",
            screen_size: Tuple[int] = (1920, 1080),
            headless: bool = False,
            require_a11y_tree: bool = True,
    ):
        """
        Args:
            path_to_vm (str): path to .vmx file
            action_space (str): "computer_13" | "pyautogui"
            tmp_dir (str): temporary directory to store trajectory stuffs like
              the extracted screenshots
            cache_dir (str): cache directory to cache task-related stuffs like
              reference file for evaluation
        """

        # Initialize environment variables
        self.path_to_vm = os.path.abspath(os.path.expandvars(os.path.expanduser(path_to_vm)))
        self.snapshot_name = snapshot_name
        self.tmp_dir_base: str = tmp_dir
        self.cache_dir_base: str = cache_dir
        self.vm_screen_size = screen_size  # todo: add the logic to get the screen size from the VM
        self.headless = headless
        self.require_a11y_tree = require_a11y_tree

        os.makedirs(self.tmp_dir_base, exist_ok=True)

        # Initialize emulator and controller
        logger.info("Initializing...")
        self._start_emulator()
        self.vm_ip = self._get_vm_ip()
        self.controller = PythonController(vm_ip=self.vm_ip)
        self.setup_controller = SetupController(vm_ip=self.vm_ip, cache_dir=self.cache_dir_base)

        # Meta info of the VM, move to the reset() function
        self.vm_platform: str = ""  # self.controller.get_vm_platform()

        # mode: human or machine
        assert action_space in ["computer_13", "pyautogui"]
        self.action_space = action_space
        # todo: define the action space and the observation space as gym did, or extend theirs

        # episodic stuffs, like tmp dir and counters, will be updated or reset
        # when calling self.reset()
        self.tmp_dir: str = self.tmp_dir_base  # just an init value, updated during reset
        self._traj_no: int = -1
        self._step_no: int = 0
        self.action_history: List[Dict[str, any]] = []

    def _start_emulator(self):
        while True:
            try:
                output = subprocess.check_output("vmrun -T ws list", shell=True, stderr=subprocess.STDOUT)
                output = output.decode()
                output: List[str] = output.splitlines()
                # if self.path_to_vm.lstrip("~/") in output:
                if self.path_to_vm in output:
                    logger.info("VM is running.")
                    break
                else:
                    logger.info("Starting VM...")
                    _execute_command(["vmrun", "-T", "ws", "start", self.path_to_vm]) if not self.headless \
                        else _execute_command(["vmrun", "-T", "ws", "start", self.path_to_vm, "nogui"])
                    time.sleep(3)
            except subprocess.CalledProcessError as e:
                logger.error(f"Error executing command: {e.output.decode().strip()}")

    def _get_vm_ip(self):
        max_retries = 20
        logger.info("Getting IP Address...")
        for _ in range(max_retries):
            try:
                output = _execute_command(["vmrun", "-T", "ws", "getGuestIPAddress", self.path_to_vm, "-wait"]).strip()
                logger.info(f"IP address: {output}")
                return output
            except Exception as e:
                print(e)
                time.sleep(5)
                logger.info("Retrying...")
        raise Exception("Failed to get VM IP address!")

    def _save_state(self):
        _execute_command(["vmrun", "-T", "ws" "snapshot", self.path_to_vm, self.snapshot_name])

    def _get_screenshot(self):
        # random_uuid = str(uuid.uuid4())
        # os.makedirs(os.path.join("tmp", random_uuid), exist_ok=True)
        # image_path = os.path.join("tmp", random_uuid, "screenshot.png")
        image_path: str = os.path.join(self.tmp_dir, "screenshots", "{:d}.png".format(self._step_no))

        # Get the screenshot and save to the image_path
        max_retries = 20
        for _ in range(max_retries):
            screenshot = self.controller.get_screenshot()
            if screenshot is not None:
                break
            time.sleep(1)

        with open(image_path, "wb") as f:
            f.write(screenshot)

        return image_path

    def _get_obs(self):
        screenshot_image_path = self._get_screenshot()
        return screenshot_image_path

    def _set_task_info(self, task_config: Dict[str, Any]):
        self.task_id: str = task_config["id"]
        self.cache_dir: str = os.path.join(self.cache_dir_base, self.task_id)
        os.makedirs(self.cache_dir, exist_ok=True)
        self.instruction = task_config["instruction"]
        self.config = task_config["config"] if "config" in task_config else []

        # evaluator dict
        # func -> metric function string, or list of metric function strings
        # conj -> conjunction of multiple metrics if func is a list with length > 1, "and"/"or"
        # result -> result getter config, or list of result getter configs
        # expected (optional) -> expected getter config, or list of expected getter configs
        # options (optional) -> metric options, or list of metric options
        # if func is a str list, then result, expected (if exists), options (if exists) should also be lists of the same length
        # even if one of the metrics does not need expected or options field, it should be included in the list with None
        self.evaluator = task_config["evaluator"]
        self.metric: Metric = [getattr(metrics, func) for func in self.evaluator["func"]] \
            if isinstance(self.evaluator["func"], list) \
            else getattr(metrics, self.evaluator["func"])
        self.metric_conj: str = self.evaluator.get("conj", "and")  # take conjunction of multiple metrics
        if "result" in self.evaluator and len(self.evaluator["result"])>0:
            self.result_getter: Getter = [getattr(getters, "get_{:}".format(res["type"])) for res in
                                          self.evaluator["result"]] \
                if isinstance(self.evaluator["result"], list) \
                else getattr(getters, "get_{:}".format(self.evaluator["result"]["type"]))
        else:
            self.result_getter = [None] * len(self.metric) \
                if isinstance(self.metric, list) \
                else None

        if "expected" in self.evaluator and len(self.evaluator["expected"])>0:
            self.expected_getter: Getter = [getattr(getters, "get_{:}".format(exp["type"])) if exp else None for exp in
                                            self.evaluator["expected"]] \
                if isinstance(self.evaluator["expected"], list) \
                else getattr(getters, "get_{:}".format(self.evaluator["expected"]["type"]))
        else:
            self.expected_getter = [None] * len(self.metric) \
                if isinstance(self.metric, list) \
                else None
        self.metric_options: Union[List[Dict[str, Any]], Dict[str, Any]] = [opt if opt else {} for opt in
                                                                            self.evaluator["options"]] \
            if isinstance(self.evaluator.get("options", {}), list) \
            else self.evaluator["options"] \
            if "options" in self.evaluator \
            else [{}] * len(self.metric) \
            if isinstance(self.metric, list) \
            else {}

        assert (not isinstance(self.evaluator["func"], list)
                or (len(self.metric) == len(self.result_getter) == len(self.expected_getter) == len(
                    self.metric_options)))

    def reset(self, task_config: Optional[Dict[str, Any]] = None, seed=None, options=None) -> Dict[str, Any]:
        logger.info("Resetting environment...")

        logger.info("Switching task...")
        if task_config is not None:
            self._set_task_info(task_config)
            self.setup_controller.reset_cache_dir(self.cache_dir)

        logger.info("Setting counters...")
        self._traj_no += 1
        self._step_no = 0
        self.action_history.clear()

        logger.info("Setup new temp dir...")
        self.tmp_dir = tempfile.mkdtemp(
            prefix="{:d}.{:}.".format(self._traj_no, self.task_id),
            dir=self.tmp_dir_base
        )
        os.makedirs(os.path.join(self.tmp_dir, "screenshots"))

        logger.info("Reverting to snapshot to {}...".format(self.snapshot_name))
        _execute_command(["vmrun", "-T", "ws", "revertToSnapshot", self.path_to_vm, self.snapshot_name])
        time.sleep(5)

        print(self.vm_screen_size)
        logger.info("Starting emulator...")
        self._start_emulator()
        logger.info("Emulator started.")

        logger.info("Get meta info of the VM...")
        self.vm_platform = self.controller.get_vm_platform()
        self.vm_screen_size = self.controller.get_vm_screen_size()
        print(self.vm_screen_size)

        logger.info("Setting up environment...")
        self.setup_controller.setup(self.config)

        time.sleep(5)
        logger.info("Environment setup complete.")

        observation = {
            "screenshot": self._get_obs(),
            "accessibility_tree": self.controller.get_accessibility_tree() if self.require_a11y_tree else None,
        }
        return observation

    def step(self, action, pause=0.5):
        self._step_no += 1
        self.action_history.append(action)

        reward = 0  # todo: Define reward calculation for each example
        done = False  # todo: Define episode termination condition for each example
        info = {}

        # handle the special actions
        if action in ['WAIT', 'FAIL', 'DONE']:
            if action == 'WAIT':
                time.sleep(pause)
            elif action == 'FAIL':
                done = True
                info = {"fail": True}
            elif action == 'DONE':
                done = True
                info = {"done": True}

        # fixme: add reminding logic here, decide if the action is valid for the current action_space
        if self.action_space == "computer_13":
            # the set of all possible actions defined in the action representation
            self.controller.execute_action(action)
        elif self.action_space == "pyautogui":
            if action in ['WAIT', 'FAIL', 'DONE']:
                self.controller.execute_action(action)
            else:
                # the set of all possible python commands insides `pyautogui`
                self.controller.execute_python_command(action)

        observation = {
            "screenshot": self._get_obs(),
            "accessibility_tree": self.controller.get_accessibility_tree() if self.require_a11y_tree else None,
            # "terminal": self.controller.get_terminal_output(),
            "instruction": self.instruction
        }

        return observation, reward, done, info

    def evaluate(self):
        """
        Evaluate whether the task is successfully completed.
        """

        self.setup_controller.setup(self.evaluator.get("postconfig", []))

        if self.evaluator['func'] == "infeasible":
            if len(self.action_history) > 0 and self.action_history[-1] == "FAIL":
                return 1
            else:
                return 0
        else:
            if len(self.action_history) > 0 and self.action_history[-1] == "FAIL":
                return 0

        if type(self.metric) == list:
            results = []
            for idx, metric in enumerate(self.metric):
                try:
                    config = self.evaluator["result"][idx]
                    result_state = self.result_getter[idx](self, config)
                except FileNotFoundError:
                    logger.error("File not found!")
                    if self.metric_conj == 'and':
                        return 0

                expected = self.evaluator["expected"][idx]
                expected_state = self.expected_getter[idx](self, expected) if expected else None

                metric: int = metric(result_state, expected_state,
                                     **self.metric_options[idx]) if expected_state is not None \
                    else metric(result_state, **self.metric_options[idx])

                if self.metric_conj == 'and' and float(metric) == 0.0:
                    return 0
                elif self.metric_conj == 'or' and float(metric) == 1.0:
                    return 1
                else:
                    results.append(metric)
            return sum(results) / len(results) if self.metric_conj == 'and' else max(results)
        else:
            try:
                result_state = self.result_getter(self, self.evaluator["result"])
            except FileNotFoundError:
                logger.error("File not found!")
                return 0

            expected_state = self.expected_getter(self, self.evaluator["expected"]) if "expected" in self.evaluator \
                else None

            metric: float = self.metric(result_state, expected_state,
                                        **self.metric_options) if expected_state is not None \
                else self.metric(result_state, **self.metric_options)

        return metric

    def render(self, mode='rgb_array'):
        if mode == 'rgb_array':
            return self._get_obs()
        else:
            raise ValueError('Unsupported render mode: {}'.format(mode))

    def close(self):
        _execute_command(["vmrun", "stop", self.path_to_vm])

```

## desktop_env/envs/__init__.py

```python

```

## desktop_env/evaluators/README.md

```markdown
# Evaluator Setup Details
Setup scaffolding for the evaluators in the desktop environment for those who want to know the details of the evaluator setup for customized evaluation and extension

## Overall
Inside the virtual machine, disable the system crash report by:
	```
	sudo vim /etc/default/apport
	```
and then change the `enabled` to `0`.

## VSCode 
todo

## LibreOffice
For LibreOffice, please enter into the app first, and then enable the no pop-up when 'ctrl + s'.

## LibreOffice Press
### Setting Up the python-pptx Library
	```shell
	pip install python-pptx
	```

## LibreOffice Writer

### Setting Up the python-docx and odfpy Library
	```shell
	pip install python-docx
	pip install odfpy
	```

## LibreOffice Calc

### Required Libraries

	```
	openpyxl
	pandas
	lxml
	xmltodict
	```

### How to Generate CSV from XLSX

	```sh
	libreoffice --convert-to "csv:Text - txt - csv (StarCalc):44,34,UTF8,,,,false,true,true,false,false,1" --out-dir /home/user /home/user/abc.xlsx
	```

This command will generate `abc-Sheet1.csv` under `/home/user`. The last `1` in
the conversion options indicates the sheet number (starting from 1) to export.
Detailed usage should be referred to at [CSV Filter
Options](https://help.libreoffice.org/latest/ro/text/shared/guide/csv_params.html).

Refer to `libreoffice_calc/21df9241-f8d7-4509-b7f1-37e501a823f7.json` for an
example.

### About `compare_table`

Evaluation to xlsx files mainly relies on `compare_table`. It accepts two file
names and a list of rules defined as `options`. Refer to
`libreoffice_calc/21df9241-f8d7-4509-b7f1-37e501a823f7.json` for an example.

In each rule, there is a required field `type`. The supported types are defined
in `compare_table` function. The most common two are `sheet_data` and
`sheet_print`. `sheet_data` compares the internal cell values through pandoc,
while `sheet_print` compares the shown cell values through csv. A csv should be
generated and downloaded for `sheet_print`. See the previous section and
example in `libreoffice_calc/21df9241-f8d7-4509-b7f1-37e501a823f7.json`.

Other fields in a rule are described for each evaluation type in
`compare_table` function. `sheet_idx0` (or `sheet_idx1`, `sheet_idx`) is a
common field to indicate which sheet is to extracted from the workbook. If an
integer i is given, then it extracts the i-th sheet from result xlsx (i starts
from 0). If a string is given, it should be preceded with "RI", "RN", "EI", or
"EN". "R" indicates to extract from result xlsx while "E" indicates to extract
from expected (golden) xlsx. "I" indicates a sheet number (starting from 0) and
"N" indicates a sheet name (usually, they're like "Sheet1", "Sheet2", ...).

Some rules use a atructure like `{"method": "eq", "ref": "abc"}`. These rules
are checked through `utils._match_value_to_rule` function. Check it for the
implemented matching methods.

## Chrome

### Starting Chrome with Remote Debugging for Python

To enable remote debugging in Chrome, which allows tools like Playwright for Python to connect to and control an existing Chrome instance, follow these steps:

#### Manually Enabling Remote Debugging in Chrome

1. **Locate the Chrome Shortcut**:
   - Find the Chrome shortcut that you usually use to open the browser. This could be on your desktop, start menu, or taskbar.

2. **Edit Shortcut Properties**:
   - Right-click on the Chrome shortcut and select `Properties`.

3. **Modify the Target Field**:
   - In the `Target` field, add `--remote-debugging-port=9222` at the end of the path. Ensure there is a space between the path and the flag you add.
   - It should look something like this: `"C:\Path\To\Chrome.exe" --remote-debugging-port=9222`.

4. **Apply and Close**:
   - Click `Apply` and then `OK` to close the dialog.

5. **Start Chrome**:
   - Use this modified shortcut to start Chrome. Chrome will now start with remote debugging enabled on port 9222.

6. **Confirm Remote Debugging**:
   - Open a browser and navigate to `http://localhost:9222`. If you see a webpage with information about active tabs, remote debugging is working.

---

### Setting Up Playwright for Python

Playwright for Python is a browser automation library to control Chromium, Firefox, and WebKit with a single API.

#### Installing Playwright

- Ensure you have Python installed on your system. If not, download and install it from the [Python official website](https://www.python.org/).

- Install Playwright using pip (Python Package Installer). Open a command line or terminal and run:

  ```bash
  pip install playwright
  ```

- After installing Playwright, you need to run the install command to download the necessary browser binaries:

  ```bash
  playwright install
  ```

#### Writing a Playwright Script in Python

- Create a Python file for your automation script.

- Import the Playwright module at the beginning of your script:

  ```python
  from playwright.sync_api import sync_playwright
  ```

- You can now use Playwright's API to control browsers.

#### Example Playwright Script

Here is a simple example to open a page using Playwright:

	```python
	from playwright.sync_api import sync_playwright
	
	def run(playwright):
	    browser = playwright.chromium.launch()
	    page = browser.new_page()
	    page.goto("http://example.com")
	    ## other actions...
	    browser.close()
	
	with sync_playwright() as playwright:
	    run(playwright)
	```

- This script launches Chromium, opens a new page, navigates to `example.com`, and then closes the browser.

#### Troubleshooting

- If you encounter issues with Playwright, ensure that your Python environment is correctly set up and that you have installed Playwright and its dependencies correctly.
- For detailed documentation, visit the [Playwright for Python Documentation](https://playwright.dev/python/docs/intro).


## VLC Media Player

### Bugs fix
One thing on Ubuntu need to do, enter into the `meida`>`convert/save`>select files>`convert/save`
Then enter the profile of `Audio - MP3`, change the profile for mp3, section audiocodec from "MP3" to "MPEG Audio"
Otherwise the mp3 file will be created but with 0 bytes. It's a bug of VLC.

### Setting Up VLC's HTTP Interface

To enable and use the HTTP interface in VLC Media Player for remote control and status checks, follow these steps:

#### 1. Open VLC Preferences

- Open VLC Media Player.
- Go to `Tools` > `Preferences` from the menu.

#### 2. Show All Settings

- In the Preferences window, at the bottom left corner, select `All` under `Show settings` to display advanced settings.

#### 3. Enable Main Interfaces

- In the advanced preferences, expand the `Interface` section.
- Click on `Main interfaces`.
- Check the box for `Web` to enable the HTTP interface.

#### 4. Configure Lua HTTP

- Expand the `Main interfaces` node and select `Lua`.
- Under `Lua HTTP`, set a password `password` in the `Lua HTTP` section. This password will be required to access the HTTP interface.

#### 5. Save and Restart VLC

- Click `Save` to apply the changes.
- Restart VLC Media Player for the changes to take effect.

#### 6. Accessing the HTTP Interface

- Open a web browser and go to `http://localhost:8080`.
- You will be prompted for a password. Enter the password you set in the Lua HTTP settings.
- Once logged in, you will have access to VLC's HTTP interface for remote control.

#### Packages
	```bash
	
	pip install opencv-python-headless Pillow imagehash
	```

#### Troubleshooting

- If you cannot access the HTTP interface, check if your firewall or security software is blocking the connection.
- Ensure VLC is running and the correct port (default is 8080) is being used.
- If the port is in use by another application, you may change the port number in VLC's settings.

## GIMP
Click on the "Keep" of the image loading pop-up.

```

## desktop_env/evaluators/__init__.py

```python
#from .table import compare_table

#eval_funcs = {
    #"compare_table(expected, actual)": compare_table
#}

```

## desktop_env/server/main.py

```python
import ctypes
import os
import platform
import shlex
import subprocess, signal
from pathlib import Path
from typing import Any, Optional
from typing import List, Dict, Tuple

import Xlib
import lxml.etree
import pyautogui
import requests
from PIL import Image
from Xlib import display, X
from flask import Flask, request, jsonify, send_file, abort  # , send_from_directory
from lxml.etree import _Element

platform_name: str = platform.system()

if platform_name=="Linux":
    import pyatspi
    from pyatspi import Accessible, StateType, STATE_SHOWING
    from pyatspi import Action as ATAction
    from pyatspi import Component, Document
    from pyatspi import Text as ATText
    from pyatspi import Value as ATValue

    BaseWrapper = Any
elif platform_name=="Windows":
    from pywinauto import Desktop
    from pywinauto.base_wrapper import BaseWrapper

    Accessible = Any

from pyxcursor import Xcursor

app = Flask(__name__)

pyautogui.PAUSE = 0
pyautogui.DARWIN_CATCH_UP_TIME = 0

logger = app.logger
recording_process = None  # fixme: this is a temporary solution for recording, need to be changed to support multiple-process
recording_path = "/tmp/recording.mp4"


@app.route('/setup/execute', methods=['POST'])
@app.route('/execute', methods=['POST'])
def execute_command():
    data = request.json
    # The 'command' key in the JSON request should contain the command to be executed.
    shell = data.get('shell', False)
    command = data.get('command', "" if shell else [])

    if isinstance(command, str) and not shell:
        command = shlex.split(command)

    # Expand user directory
    for i, arg in enumerate(command):
        if arg.startswith("~/"):
            command[i] = os.path.expanduser(arg)

    # Execute the command without any safety checks.
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell, text=True, timeout=120)
        return jsonify({
            'status': 'success',
            'output': result.stdout,
            'error': result.stderr,
            'returncode': result.returncode
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


def _get_machine_architecture() -> str:
    """ Get the machine architecture, e.g., x86_64, arm64, aarch64, i386, etc.
    """
    architecture = platform.machine().lower()
    if architecture in ['amd32', 'amd64', 'x86', 'x86_64', 'x86-64', 'x64', 'i386', 'i686']:
        return 'amd'
    elif architecture in ['arm64', 'aarch64', 'aarch32']:
        return 'arm'
    else:
        return 'unknown'


@app.route('/setup/launch', methods=["POST"])
def launch_app():
    data = request.json
    shell = data.get("shell", False)
    command: List[str] = data.get("command", "" if shell else [])

    if isinstance(command, str) and not shell:
        command = shlex.split(command)

    # Expand user directory
    for i, arg in enumerate(command):
        if arg.startswith("~/"):
            command[i] = os.path.expanduser(arg)

    try:
        if 'google-chrome' in command and _get_machine_architecture() == 'arm':
            index = command.index('google-chrome')
            command[index] = 'chromium-browser' # arm64 chrome is not available yet, can only use chromium
        subprocess.Popen(command, shell=shell)
        return "{:} launched successfully".format(command if shell else " ".join(command))
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/screenshot', methods=['GET'])
def capture_screen_with_cursor():
    # fixme: when running on virtual machines, the cursor is not captured, don't know why

    file_path = os.path.join(os.path.dirname(__file__), "screenshots", "screenshot.png")
    user_platform = platform.system()

    # Ensure the screenshots directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # fixme: This is a temporary fix for the cursor not being captured on Windows and Linux
    if user_platform == "Windows":
        def _download_image(url, path):
            response = requests.get(url)
            with open(path, 'wb') as file:
                file.write(response.content)

        cursor_path = os.path.join("screenshots", "cursor.png")
        if not os.path.exists(cursor_path):
            cursor_url = "https://vip.helloimg.com/images/2023/12/02/oQPzmt.png"
            _download_image(cursor_url, cursor_path)
        screenshot = pyautogui.screenshot()
        cursor_x, cursor_y = pyautogui.position()
        cursor = Image.open(cursor_path)
        # make the cursor smaller
        cursor = cursor.resize((int(cursor.width / 1.5), int(cursor.height / 1.5)))
        screenshot.paste(cursor, (cursor_x, cursor_y), cursor)
        screenshot.save(file_path)
    elif user_platform == "Linux":
        cursor_obj = Xcursor()
        imgarray = cursor_obj.getCursorImageArrayFast()
        cursor_img = Image.fromarray(imgarray)
        screenshot = pyautogui.screenshot()
        cursor_x, cursor_y = pyautogui.position()
        screenshot.paste(cursor_img, (cursor_x, cursor_y), cursor_img)
        screenshot.save(file_path)
    elif user_platform == "Darwin":  # (Mac OS)
        # Use the screencapture utility to capture the screen with the cursor
        subprocess.run(["screencapture", "-C", file_path])
    else:
        logger.warning(f"The platform you're using ({user_platform}) is not currently supported")

    return send_file(file_path, mimetype='image/png')


def _has_active_terminal(desktop: Accessible) -> bool:
    """ A quick check whether the terminal window is open and active.
    """
    for app in desktop:
        if app.getRoleName() == "application" and app.name == "gnome-terminal-server":
            for frame in app:
                if frame.getRoleName() == "frame" and frame.getState().contains(pyatspi.STATE_ACTIVE):
                    return True
    return False


@app.route('/terminal', methods=['GET'])
def get_terminal_output():
    user_platform = platform.system()
    output: Optional[str] = None
    try:
        if user_platform == "Linux":
            desktop: Accessible = pyatspi.Registry.getDesktop(0)
            if _has_active_terminal(desktop):
                desktop_xml: _Element = _create_atspi_node(desktop)
                # 1. the terminal window (frame of application is st:active) is open and active
                # 2. the terminal tab (terminal status is st:focused) is focused
                xpath = '//application[@name="gnome-terminal-server"]/frame[@st:active="true"]//terminal[@st:focused="true"]'
                terminals: List[_Element] = desktop_xml.xpath(xpath, namespaces=_accessibility_ns_map)
                output = terminals[0].text.rstrip() if len(terminals) == 1 else None
        else:  # windows and macos platform is not implemented currently
            # raise NotImplementedError
            return "Currently not implemented for platform {:}.".format(platform.platform()), 500
        return jsonify({"output": output, "status": "success"})
    except Exception as e:
        logger.error("Failed to get terminal output. Error: %s", e)
        return jsonify({"status": "error", "message": str(e)}), 500


_accessibility_ns_map = { "st": "uri:deskat:state.at-spi.gnome.org"
                        , "attr": "uri:deskat:attributes.at-spi.gnome.org"
                        , "cp": "uri:deskat:component.at-spi.gnome.org"
                        , "doc": "uri:deskat:document.at-spi.gnome.org"
                        , "docattr": "uri:deskat:attributes.document.at-spi.gnome.org"
                        , "txt": "uri:deskat:text.at-spi.gnome.org"
                        , "val": "uri:deskat:value.at-spi.gnome.org"
                        , "act": "uri:deskat:action.at-spi.gnome.org"
                        , "win": "uri:deskat:uia.windows.microsoft.org"
                        }


def _create_atspi_node(node: Accessible, depth: int = 0, flag: Optional[str] = None) -> _Element:
    #  function _create_atspi_node {{{ # 
    if node.getRoleName() == "document spreadsheet":
        flag = "calc"
    if node.getRoleName() == "application" and node.name=="Thunderbird":
        flag = "thunderbird"

    attribute_dict: Dict[str, Any] = {"name": node.name}

    #  States {{{ # 
    states: List[StateType] = node.getState().get_states()
    for st in states:
        state_name: str = StateType._enum_lookup[st]
        if len(state_name.split("_", maxsplit=1)[1].lower()) == 0:
            continue
        attribute_dict[
            "{{{:}}}{:}".format(_accessibility_ns_map["st"], state_name.split("_", maxsplit=1)[1].lower())] = "true"
    #  }}} States # 

    #  Attributes {{{ # 
    attributes: List[str] = node.getAttributes()
    for attrbt in attributes:
        attribute_name: str
        attribute_value: str
        attribute_name, attribute_value = attrbt.split(":", maxsplit=1)
        if len(attribute_name) == 0:
            continue
        attribute_dict["{{{:}}}{:}".format(_accessibility_ns_map["attr"], attribute_name)] = attribute_value
    #  }}} Attributes # 

    #  Component {{{ # 
    try:
        component: Component = node.queryComponent()
    except NotImplementedError:
        pass
    else:
        attribute_dict["{{{:}}}screencoord".format(_accessibility_ns_map["cp"])] = str(
            component.getPosition(pyatspi.XY_SCREEN))
        attribute_dict["{{{:}}}windowcoord".format(_accessibility_ns_map["cp"])] = str(
            component.getPosition(pyatspi.XY_WINDOW))
        attribute_dict["{{{:}}}parentcoord".format(_accessibility_ns_map["cp"])] = str(
            component.getPosition(pyatspi.XY_PARENT))
        attribute_dict["{{{:}}}size".format(_accessibility_ns_map["cp"])] = str(component.getSize())
    #  }}} Component # 

    #  Document {{{ # 
    try:
        document: Document = node.queryDocument()
    except NotImplementedError:
        pass
    else:
        attribute_dict["{{{:}}}locale".format(_accessibility_ns_map["doc"])] = document.getLocale()
        attribute_dict["{{{:}}}pagecount".format(_accessibility_ns_map["doc"])] = str(document.getPageCount())
        attribute_dict["{{{:}}}currentpage".format(_accessibility_ns_map["doc"])] = str(document.getCurrentPageNumber())
        for attrbt in document.getAttributes():
            attribute_name: str
            attribute_value: str
            attribute_name, attribute_value = attrbt.split(":", maxsplit=1)
            if len(attribute_name) == 0:
                continue
            attribute_dict["{{{:}}}{:}".format(_accessibility_ns_map["docattr"], attribute_name)] = attribute_value
    #  }}} Document # 

    #  Text {{{ # 
    try:
        text_obj: ATText = node.queryText()
    except NotImplementedError:
        pass
    else:
        # only text shown on current screen is available
        # attribute_dict["txt:text"] = text_obj.getText(0, text_obj.characterCount)
        text: str = text_obj.getText(0, text_obj.characterCount)
        #if flag=="thunderbird":
        # appeard in thunderbird (uFFFC) (not only in thunderbird), "Object
        # Replacement Character" in Unicode, "used as placeholder in text for
        # an otherwise unspecified object; uFFFD is another "Replacement
        # Character", just in case
        text = text.replace("\ufffc", "").replace("\ufffd", "")
    #  }}} Text # 

    #  Image {{{ # 
    try:
        node.queryImage()
    except NotImplementedError:
        pass
    else:
        attribute_dict["image"] = "true"
    #  }}} Image # 

    #  Selection {{{ # 
    try:
        node.querySelection()
    except NotImplementedError:
        pass
    else:
        attribute_dict["selection"] = "true"
    #  }}} Selection # 

    #  Value {{{ # 
    try:
        value: ATValue = node.queryValue()
    except NotImplementedError:
        pass
    else:
        try:
            attribute_dict["{{{:}}}value".format(_accessibility_ns_map["val"])] = str(value.currentValue)
        except:
            pass
        try:
            attribute_dict["{{{:}}}min".format(_accessibility_ns_map["val"])] = str(value.minimumValue)
        except:
            pass
        try:
            attribute_dict["{{{:}}}max".format(_accessibility_ns_map["val"])] = str(value.maximumValue)
        except:
            pass
        try:
            attribute_dict["{{{:}}}step".format(_accessibility_ns_map["val"])] = str(value.minimumIncrement)
        except:
            pass
    #  }}} Value # 

    #  Action {{{ # 
    try:
        action: ATAction = node.queryAction()
    except NotImplementedError:
        pass
    else:
        for i in range(action.nActions):
            action_name: str = action.getName(i).replace(" ", "-")
            attribute_dict["{{{:}}}{:}_desc" \
                .format(_accessibility_ns_map["act"]
                        , action_name
                        )
            ] = action.getDescription(i)
            attribute_dict["{{{:}}}{:}_kb" \
                .format(_accessibility_ns_map["act"]
                        , action_name
                        )
            ] = action.getKeyBinding(i)
    #  }}} Action #

    if node.getRoleName().strip() == "":
        node_role_name = "unknown"
    else:
        node_role_name = node.getRoleName().replace(" ", "-")

    xml_node = lxml.etree.Element(
        node_role_name,
        attrib=attribute_dict,
        nsmap=_accessibility_ns_map
    )
    if "text" in locals() and len(text) > 0:
        xml_node.text = text

    # HYPERPARAMETER
    if depth==50:
        logger.warning("Max depth reached")
        return xml_node

    if flag=="calc" and node_role_name=="table":
        # Maximum column: 1024 if ver<=7.3 else 16384
        # Maximum row: 104 8576
        # Maximun sheet: 1 0000

        version_str: str = subprocess.run("libreoffice --version", shell=True, text=True, stdout=subprocess.PIPE).stdout
        version_str = version_str.split()[1]
        version_tuple: Tuple[int] = tuple(map(int, version_str.split(".")))
        MAXIMUN_COLUMN = 1024 if version_tuple<(7, 4) else 16384
        MAX_ROW = 104_8576

        index_base = 0
        first_showing = False
        column_base = None
        for r in range(MAX_ROW):
            #logger.warning(r)
            for clm in range(column_base or 0, MAXIMUN_COLUMN):
                child_node: Accessible = node[index_base+clm]
                showing: bool = child_node.getState().contains(STATE_SHOWING)
                if showing:
                    child_node: _Element = _create_atspi_node(child_node, depth+1, flag)
                    if not first_showing:
                        column_base = clm
                        first_showing = True
                    xml_node.append(child_node)
                elif first_showing and column_base is not None or clm>=500:
                    break
            if first_showing and clm==column_base or not first_showing and r>=500:
                break
            index_base += MAXIMUN_COLUMN
        return xml_node
    else:
        try:
            for i, ch in enumerate(node):
                # HYPERPARAMETER
                if i>=1025:
                    logger.warning("Max width reached")
                    break
                xml_node.append(_create_atspi_node(ch, depth+1, flag))
        except:
            logger.warning("Error occurred during children traversing. Has Ignored. Node: %s", lxml.etree.tostring(xml_node, encoding="unicode"))
        return xml_node
    #  }}} function _create_atspi_node # 

def _create_pywinauto_node(node: BaseWrapper, depth: int = 0, flag: Optional[str] = None) -> _Element:
    #  function _create_pywinauto_node {{{ # 
    #element_info: ElementInfo = node.element_info
    attribute_dict: Dict[str, Any] = {"name": node.element_info.name}

    #  States {{{ # 
    try:
        attribute_dict["{{{:}}}enabled".format(_accessibility_ns_map["st"])] = str(node.is_enabled()).lower()
    except:
        pass
    try:
        attribute_dict["{{{:}}}visible".format(_accessibility_ns_map["st"])] = str(node.is_visible()).lower()
    except:
        pass
    try:
        attribute_dict["{{{:}}}active".format(_accessibility_ns_map["st"])] = str(node.is_active()).lower()
    except:
        pass

    if hasattr(node, "is_minimized"):
        try:
            attribute_dict["{{{:}}}minimized".format(_accessibility_ns_map["st"])] = str(node.is_minimized()).lower()
        except:
            pass
    if hasattr(node, "is_maximized"):
        try:
            attribute_dict["{{{:}}}maximized".format(_accessibility_ns_map["st"])] = str(node.is_maximized()).lower()
        except:
            pass
    if hasattr(node, "is_normal"):
        try:
            attribute_dict["{{{:}}}normal".format(_accessibility_ns_map["st"])] = str(node.is_normal()).lower()
        except:
            pass

    if hasattr(node, "is_unicode"):
        try:
            attribute_dict["{{{:}}}unicode".format(_accessibility_ns_map["st"])] = str(node.is_unicode()).lower()
        except:
            pass

    if hasattr(node, "is_collapsed"):
        try:
            attribute_dict["{{{:}}}collapsed".format(_accessibility_ns_map["st"])] = str(node.is_collapsed()).lower()
        except:
            pass
    if hasattr(node, "is_checkable"):
        try:
            attribute_dict["{{{:}}}checkable".format(_accessibility_ns_map["st"])] = str(node.is_checkable()).lower()
        except:
            pass
    if hasattr(node, "is_checked"):
        try:
            attribute_dict["{{{:}}}checked".format(_accessibility_ns_map["st"])] = str(node.is_checked()).lower()
        except:
            pass
    if hasattr(node, "is_focused"):
        try:
            attribute_dict["{{{:}}}focused".format(_accessibility_ns_map["st"])] = str(node.is_focused()).lower()
        except:
            pass
    if hasattr(node, "is_keyboard_focused"):
        try:
            attribute_dict["{{{:}}}keyboard_focused".format(_accessibility_ns_map["st"])] = str(node.is_keyboard_focused()).lower()
        except:
            pass
    if hasattr(node, "is_selected"):
        try:
            attribute_dict["{{{:}}}selected".format(_accessibility_ns_map["st"])] = str(node.is_selected()).lower()
        except:
            pass
    if hasattr(node, "is_selection_required"):
        try:
            attribute_dict["{{{:}}}selection_required".format(_accessibility_ns_map["st"])] = str(node.is_selection_required()).lower()
        except:
            pass
    if hasattr(node, "is_pressable"):
        try:
            attribute_dict["{{{:}}}pressable".format(_accessibility_ns_map["st"])] = str(node.is_pressable()).lower()
        except:
            pass
    if hasattr(node, "is_pressed"):
        try:
            attribute_dict["{{{:}}}pressed".format(_accessibility_ns_map["st"])] = str(node.is_pressed()).lower()
        except:
            pass

    if hasattr(node, "is_expanded"):
        try:
            attribute_dict["{{{:}}}expanded".format(_accessibility_ns_map["st"])] = str(node.is_expanded()).lower()
        except:
            pass
    if hasattr(node, "is_editable"):
        try:
            attribute_dict["{{{:}}}editable".format(_accessibility_ns_map["st"])] = str(node.is_editable()).lower()
        except:
            pass
    #  }}} States # 

    #  Component {{{ # 
    rectangle = node.rectangle()
    attribute_dict["{{{:}}}screencoord".format(_accessibility_ns_map["cp"])] = "({:d}, {:d})".format(rectangle.left, rectangle.top)
    attribute_dict["{{{:}}}size".format(_accessibility_ns_map["cp"])] = "({:d}, {:d})".format(rectangle.width(), rectangle.height())
    #  }}} Component # 

    #  Text {{{ # 
    text: str = node.window_text()
    if text==attribute_dict["name"]:
        text = ""
    #if hasattr(node, "texts"):
        #texts: List[str] = node.texts()[1:]
        #texts: Iterable[str] = map(lambda itm: itm if isinstance(itm, str) else "".join(itm), texts)
    #text += "\n".join(texts)
    #text = text.strip()
    #  }}} Text # 

    #  Selection {{{ # 
    if hasattr(node, "select"):
        attribute_dict["selection"] = "true"
    #  }}} Selection # 

    #  Value {{{ # 
    if hasattr(node, "get_step"):
        try:
            attribute_dict["{{{:}}}step".format(_accessibility_ns_map["val"])] = str(node.get_step())
        except:
            pass
    if hasattr(node, "value"):
        try:
            attribute_dict["{{{:}}}value".format(_accessibility_ns_map["val"])] = str(node.value())
        except:
            pass
    if hasattr(node, "get_value"):
        try:
            attribute_dict["{{{:}}}value".format(_accessibility_ns_map["val"])] = str(node.get_value())
        except:
            pass
    elif hasattr(node, "get_position"):
        try:
            attribute_dict["{{{:}}}value".format(_accessibility_ns_map["val"])] = str(node.get_position())
        except:
            pass
    if hasattr(node, "min_value"):
        try:
            attribute_dict["{{{:}}}min".format(_accessibility_ns_map["val"])] = str(node.min_value())
        except:
            pass
    elif hasattr(node, "get_range_min"):
        try:
            attribute_dict["{{{:}}}min".format(_accessibility_ns_map["val"])] = str(node.get_range_min())
        except:
            pass
    if hasattr(node, "max_value"):
        try:
            attribute_dict["{{{:}}}max".format(_accessibility_ns_map["val"])] = str(node.max_value())
        except:
            pass
    elif hasattr(node, "get_range_max"):
        try:
            attribute_dict["{{{:}}}max".format(_accessibility_ns_map["val"])] = str(node.get_range_max())
        except:
            pass
    #  }}} Value # 

    attribute_dict["{{{:}}}class".format(_accessibility_ns_map["win"])] = str(type(node))

    node_role_name: str = node.class_name().lower().replace(" ", "-")
    node_role_name = "".join( map( lambda ch: ch if ch.isidentifier()\
                                                 or ch in {"-"}\
                                                 or ch.isalnum()
                                               else "-"
                                 , node_role_name
                                 )
                            )
    if node_role_name.strip() == "":
        node_role_name = "unknown"
    if not node_role_name[0].isalpha():
        node_role_name = "tag" + node_role_name

    xml_node = lxml.etree.Element(
        node_role_name,
        attrib=attribute_dict,
        nsmap=_accessibility_ns_map
    )
    if text is not None and len(text)>0 and text!=attribute_dict["name"]:
        xml_node.text = text

    # HYPERPARAMETER
    if depth==50:
        logger.warning("Max depth reached")
        #print("Max depth reached")
        return xml_node

    for i, ch in enumerate(node.children()):
        # HYPERPARAMETER
        if i>=2048:
            logger.warning("Max width reached")
            #print("Max width reached")
            break
        xml_node.append(_create_pywinauto_node(ch, depth+1, flag))
    return xml_node
    #  }}} function _create_pywinauto_node # 

@app.route("/accessibility", methods=["GET"])
def get_accessibility_tree():
    os_name: str = platform.system()

    # AT-SPI works for KDE as well
    if os_name == "Linux":
        desktop: Accessible = pyatspi.Registry.getDesktop(0)
        desktop_xml: _Element = _create_atspi_node(desktop, 0)
        return jsonify({"AT": lxml.etree.tostring(desktop_xml, encoding="unicode")})

    elif os_name == "Windows":
        # Windows AT may be read through `pywinauto` module, however, two different backends `win32` and `uia` are supported and different results may be returned
        desktop: Desktop = Desktop(backend="uia")
        xml_node = lxml.etree.Element("desktop", nsmap=_accessibility_ns_map)
        for wnd in desktop.windows():
            logger.debug("Win UIA AT parsing: %s(%d)", wnd.element_info.name, len(wnd.children()))
            node: _Element = _create_pywinauto_node(wnd, 1)
            xml_node.append(node)
        return jsonify({"AT": lxml.etree.tostring(xml_node, encoding="unicode")})
    else:
        return "Currently not implemented for platform {:}.".format(platform.platform()), 500


@app.route('/screen_size', methods=['POST'])
def get_screen_size():
    if platform_name=="Linux":
        d = display.Display()
        screen_width = d.screen().width_in_pixels
        screen_height = d.screen().height_in_pixels
    elif platform_name=="Windows":
        user32 = ctypes.windll.user32
        screen_width: int = user32.GetSystemMetrics(0)
        screen_height: int = user32.GetSystemMetrics(1)
    return jsonify(
        {
            "width": screen_width,
            "height": screen_height
        }
    )


@app.route('/window_size', methods=['POST'])
def get_window_size():
    if 'app_class_name' in request.form:
        app_class_name = request.form['app_class_name']
    else:
        return jsonify({"error": "app_class_name is required"}), 400

    d = display.Display()
    root = d.screen().root
    window_ids = root.get_full_property(d.intern_atom('_NET_CLIENT_LIST'), X.AnyPropertyType).value

    for window_id in window_ids:
        try:
            window = d.create_resource_object('window', window_id)
            wm_class = window.get_wm_class()

            if wm_class is None:
                continue

            if app_class_name.lower() in [name.lower() for name in wm_class]:
                geom = window.get_geometry()
                return jsonify(
                    {
                        "width": geom.width,
                        "height": geom.height
                    }
                )
        except Xlib.error.XError:  # Ignore windows that give an error
            continue
    return None


@app.route('/desktop_path', methods=['POST'])
def get_desktop_path():
    # Get the home directory in a platform-independent manner using pathlib
    home_directory = str(Path.home())

    # Determine the desktop path based on the operating system
    desktop_path = {
        "Windows": os.path.join(home_directory, "Desktop"),
        "Darwin": os.path.join(home_directory, "Desktop"),  # macOS
        "Linux": os.path.join(home_directory, "Desktop")
    }.get(platform.system(), None)

    # Check if the operating system is supported and the desktop path exists
    if desktop_path and os.path.exists(desktop_path):
        return jsonify(desktop_path=desktop_path)
    else:
        return jsonify(error="Unsupported operating system or desktop path not found"), 404


@app.route('/wallpaper', methods=['POST'])
def get_wallpaper():
    def get_wallpaper_windows():
        SPI_GETDESKWALLPAPER = 0x73
        MAX_PATH = 260
        buffer = ctypes.create_unicode_buffer(MAX_PATH)
        ctypes.windll.user32.SystemParametersInfoW(SPI_GETDESKWALLPAPER, MAX_PATH, buffer, 0)
        return buffer.value

    def get_wallpaper_macos():
        script = """
        tell application "System Events" to tell every desktop to get picture
        """
        process = subprocess.Popen(['osascript', '-e', script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        if error:
            app.logger.error("Error: %s", error.decode('utf-8'))
            return None
        return output.strip().decode('utf-8')

    def get_wallpaper_linux():
        try:
            output = subprocess.check_output(
                ["gsettings", "get", "org.gnome.desktop.background", "picture-uri"],
                stderr=subprocess.PIPE
            )
            return output.decode('utf-8').strip().replace('file://', '').replace("'", "")
        except subprocess.CalledProcessError as e:
            app.logger.error("Error: %s", e)
            return None

    os_name = platform.system()
    wallpaper_path = None
    if os_name == 'Windows':
        wallpaper_path = get_wallpaper_windows()
    elif os_name == 'Darwin':
        wallpaper_path = get_wallpaper_macos()
    elif os_name == 'Linux':
        wallpaper_path = get_wallpaper_linux()
    else:
        app.logger.error(f"Unsupported OS: {os_name}")
        abort(400, description="Unsupported OS")

    if wallpaper_path:
        try:
            # Ensure the filename is secure
            return send_file(wallpaper_path, mimetype='image/png')
        except Exception as e:
            app.logger.error(f"An error occurred while serving the wallpaper file: {e}")
            abort(500, description="Unable to serve the wallpaper file")
    else:
        abort(404, description="Wallpaper file not found")


@app.route('/list_directory', methods=['POST'])
def get_directory_tree():
    def _list_dir_contents(directory):
        """
        List the contents of a directory recursively, building a tree structure.

        :param directory: The path of the directory to inspect.
        :return: A nested dictionary with the contents of the directory.
        """
        tree = {'type': 'directory', 'name': os.path.basename(directory), 'children': []}
        try:
            # List all files and directories in the current directory
            for entry in os.listdir(directory):
                full_path = os.path.join(directory, entry)
                # If entry is a directory, recurse into it
                if os.path.isdir(full_path):
                    tree['children'].append(_list_dir_contents(full_path))
                else:
                    tree['children'].append({'type': 'file', 'name': entry})
        except OSError as e:
            # If the directory cannot be accessed, return the exception message
            tree = {'error': str(e)}
        return tree

    # Extract the 'path' parameter from the JSON request
    data = request.get_json()
    if 'path' not in data:
        return jsonify(error="Missing 'path' parameter"), 400

    start_path = data['path']
    # Ensure the provided path is a directory
    if not os.path.isdir(start_path):
        return jsonify(error="The provided path is not a directory"), 400

    # Generate the directory tree starting from the provided path
    directory_tree = _list_dir_contents(start_path)
    return jsonify(directory_tree=directory_tree)


@app.route('/file', methods=['POST'])
def get_file():
    # Retrieve filename from the POST request
    if 'file_path' in request.form:
        file_path = os.path.expandvars(os.path.expanduser(request.form['file_path']))
    else:
        return jsonify({"error": "file_path is required"}), 400

    try:
        # Check if the file exists and send it to the user
        return send_file(file_path, as_attachment=True)
    except FileNotFoundError:
        # If the file is not found, return a 404 error
        return jsonify({"error": "File not found"}), 404


@app.route("/setup/upload", methods=["POST"])
def upload_file():
    # Retrieve filename from the POST request
    if 'file_path' in request.form and 'file_data' in request.files:
        file_path = os.path.expandvars(os.path.expanduser(request.form['file_path']))
        file = request.files["file_data"]
        file.save(file_path)
        return "File Uploaded"
    else:
        return jsonify({"error": "file_path and file_data are required"}), 400


@app.route('/platform', methods=['GET'])
def get_platform():
    return platform.system()


@app.route('/cursor_position', methods=['GET'])
def get_cursor_position():
    return pyautogui.position().x, pyautogui.position().y


@app.route("/setup/change_wallpaper", methods=['POST'])
def change_wallpaper():
    data = request.json
    path = data.get('path', None)

    if not path:
        return "Path not supplied!", 400

    path = Path(os.path.expandvars(os.path.expanduser(path)))

    if not path.exists():
        return f"File not found: {path}", 404

    try:
        user_platform = platform.system()
        if user_platform == "Windows":
            import ctypes
            ctypes.windll.user32.SystemParametersInfoW(20, 0, str(path), 3)
        elif user_platform == "Linux":
            import subprocess
            subprocess.run(["gsettings", "set", "org.gnome.desktop.background", "picture-uri", f"file://{path}"])
        elif user_platform == "Darwin":  # (Mac OS)
            import subprocess
            subprocess.run(
                ["osascript", "-e", f'tell application "Finder" to set desktop picture to POSIX file "{path}"'])
        return "Wallpaper changed successfully"
    except Exception as e:
        return f"Failed to change wallpaper. Error: {e}", 500


@app.route("/setup/download_file", methods=['POST'])
def download_file():
    data = request.json
    url = data.get('url', None)
    path = data.get('path', None)
    print(url, path)
    print("*" * 100)

    if not url or not path:
        return "Path or URL not supplied!", 400

    path = Path(os.path.expandvars(os.path.expanduser(path)))
    path.parent.mkdir(parents=True, exist_ok=True)

    max_retries = 3
    error: Optional[Exception] = None
    for i in range(max_retries):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            with open(path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            return "File downloaded successfully"

        except requests.RequestException as e:
            error = e
            logger.error(f"Failed to download {url}. Retrying... ({max_retries - i - 1} attempts left)")

    return f"Failed to download {url}. No retries left. Error: {error}", 500


@app.route("/setup/open_file", methods=['POST'])
def open_file():
    data = request.json
    path = data.get('path', None)

    if not path:
        return "Path not supplied!", 400

    path = Path(os.path.expandvars(os.path.expanduser(path)))

    if not path.exists():
        return f"File not found: {path}", 404

    try:
        if platform.system() == "Windows":
            os.startfile(path)
        else:
            open_cmd: str = "open" if platform.system() == "Darwin" else "xdg-open"
            subprocess.Popen([open_cmd, str(path)])
        return "File opened successfully"
    except Exception as e:
        return f"Failed to open {path}. Error: {e}", 500


@app.route("/setup/activate_window", methods=['POST'])
def activate_window():
    data = request.json
    window_name = data.get('window_name', None)
    if not window_name:
        return "window_name required", 400
    strict: bool = data.get("strict", False)  # compare case-sensitively and match the whole string
    by_class_name: bool = data.get("by_class", False)

    os_name = platform.system()

    if os_name == 'Windows':
        import pygetwindow as gw
        if by_class_name:
            return "Get window by class name is not supported on Windows currently.", 500
        windows: List[gw.Window] = gw.getWindowsWithTitle(window_name)

        window: Optional[gw.Window] = None
        if len(windows) == 0:
            return "Window {:} not found (empty results)".format(window_name), 404
        elif strict:
            for wnd in windows:
                if wnd.title == wnd:
                    window = wnd
            if window is None:
                return "Window {:} not found (strict mode).".format(window_name), 404
        else:
            window = windows[0]
        window.activate()

    elif os_name == 'Darwin':
        import pygetwindow as gw
        if by_class_name:
            return "Get window by class name is not supported on macOS currently.", 500
        # Find the VS Code window
        windows = gw.getWindowsWithTitle(window_name)

        window: Optional[gw.Window] = None
        if len(windows) == 0:
            return "Window {:} not found (empty results)".format(window_name), 404
        elif strict:
            for wnd in windows:
                if wnd.title == wnd:
                    window = wnd
            if window is None:
                return "Window {:} not found (strict mode).".format(window_name), 404
        else:
            window = windows[0]

        # Un-minimize the window and then bring it to the front
        window.unminimize()
        window.activate()

    elif os_name == 'Linux':
        # Attempt to activate VS Code window using wmctrl
        subprocess.run(["wmctrl"
                           , "-{:}{:}a".format("x" if by_class_name else ""
                                               , "F" if strict else ""
                                               )
                           , window_name
                        ]
                       )

    else:
        return f"Operating system {os_name} not supported.", 400

    return "Window activated successfully", 200


@app.route("/setup/close_window", methods=["POST"])
def close_window():
    data = request.json
    if "window_name" not in data:
        return "window_name required", 400
    window_name: str = data["window_name"]
    strict: bool = data.get("strict", False)  # compare case-sensitively and match the whole string
    by_class_name: bool = data.get("by_class", False)

    os_name: str = platform.system()
    if os_name == "Windows":
        import pygetwindow as gw

        if by_class_name:
            return "Get window by class name is not supported on Windows currently.", 500
        windows: List[gw.Window] = gw.getWindowsWithTitle(window_name)

        window: Optional[gw.Window] = None
        if len(windows) == 0:
            return "Window {:} not found (empty results)".format(window_name), 404
        elif strict:
            for wnd in windows:
                if wnd.title == wnd:
                    window = wnd
            if window is None:
                return "Window {:} not found (strict mode).".format(window_name), 404
        else:
            window = windows[0]
        window.close()
    elif os_name == "Linux":
        subprocess.run(["wmctrl"
                           , "-{:}{:}c".format("x" if by_class_name else ""
                                               , "F" if strict else ""
                                               )
                           , window_name
                        ]
                       )
    elif os_name == "Darwin":
        import pygetwindow as gw
        return "Currently not supported on macOS.", 500
    else:
        return "Not supported platform {:}".format(os_name), 500

    return "Window closed successfully.", 200


@app.route('/start_recording', methods=['POST'])
def start_recording():
    global recording_process
    if recording_process:
        return jsonify({'status': 'error', 'message': 'Recording is already in progress.'}), 400

    d = display.Display()
    screen_width = d.screen().width_in_pixels
    screen_height = d.screen().height_in_pixels

    start_command = f"ffmpeg -y -f x11grab -draw_mouse 1 -s {screen_width}x{screen_height} -i :0.0 -c:v libx264 -r 30 {recording_path}"

    recording_process = subprocess.Popen(shlex.split(start_command), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    return jsonify({'status': 'success', 'message': 'Started recording.'})


@app.route('/end_recording', methods=['POST'])
def end_recording():
    global recording_process

    if not recording_process:
        return jsonify({'status': 'error', 'message': 'No recording in progress to stop.'}), 400

    recording_process.send_signal(signal.SIGINT)
    recording_process.wait()
    recording_process = None

    # return recording video file
    if os.path.exists(recording_path):
        return send_file(recording_path, as_attachment=True)
    else:
        return abort(404, description="Recording failed")


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

```

## desktop_env/server/osbench_server.service

```
[Unit]
Description=OSBench Server
StartLimitIntervalSec=60
StartLimitBurst=4
After=network.target auditd.service

[Service]
ExecStart=/usr/bin/python3 /home/user/main.py
User=user
WorkingDirectory=/home/user
Restart=on-failure
RestartSec=1
Environment="DISPLAY=:1"

[Install]
WantedBy=graphical.target

```

## desktop_env/server/osbench_server@.service

```
[Unit]
Description=OSBench Server
StartLimitIntervalSec=60
StartLimitBurst=4
After=network.target auditd.service

[Service]
ExecStart=/usr/bin/python3 /home/user/main.py
User=user
WorkingDirectory=/home/user
Restart=on-failure
RestartSec=1
Environment="DISPLAY=%i"

[Install]
WantedBy=graphical.target

```

## desktop_env/server/pyxcursor.py

```python
import os
import ctypes
import ctypes.util
import numpy as np

# A helper function to convert data from Xlib to byte array.
import struct, array

# Define ctypes version of XFixesCursorImage structure.
PIXEL_DATA_PTR = ctypes.POINTER(ctypes.c_ulong)
Atom = ctypes.c_ulong


class XFixesCursorImage(ctypes.Structure):
    """
    See /usr/include/X11/extensions/Xfixes.h

    typedef struct {
        short	    x, y;
        unsigned short  width, height;
        unsigned short  xhot, yhot;
        unsigned long   cursor_serial;
        unsigned long   *pixels;
    if XFIXES_MAJOR >= 2
        Atom	    atom;	/* Version >= 2 only */
        const char	*name;	/* Version >= 2 only */
    endif
    } XFixesCursorImage;
    """
    _fields_ = [('x', ctypes.c_short),
                ('y', ctypes.c_short),
                ('width', ctypes.c_ushort),
                ('height', ctypes.c_ushort),
                ('xhot', ctypes.c_ushort),
                ('yhot', ctypes.c_ushort),
                ('cursor_serial', ctypes.c_ulong),
                ('pixels', PIXEL_DATA_PTR),
                ('atom', Atom),
                ('name', ctypes.c_char_p)]


class Display(ctypes.Structure):
    pass


class Xcursor:
    display = None

    def __init__(self, display=None):
        if not display:
            try:
                display = os.environ["DISPLAY"].encode("utf-8")
            except KeyError:
                raise Exception("$DISPLAY not set.")

        # XFixeslib = ctypes.CDLL('libXfixes.so')
        XFixes = ctypes.util.find_library("Xfixes")
        if not XFixes:
            raise Exception("No XFixes library found.")
        self.XFixeslib = ctypes.cdll.LoadLibrary(XFixes)

        # xlib = ctypes.CDLL('libX11.so.6')
        x11 = ctypes.util.find_library("X11")
        if not x11:
            raise Exception("No X11 library found.")
        self.xlib = ctypes.cdll.LoadLibrary(x11)

        # Define ctypes' version of XFixesGetCursorImage function
        XFixesGetCursorImage = self.XFixeslib.XFixesGetCursorImage
        XFixesGetCursorImage.restype = ctypes.POINTER(XFixesCursorImage)
        XFixesGetCursorImage.argtypes = [ctypes.POINTER(Display)]
        self.XFixesGetCursorImage = XFixesGetCursorImage

        XOpenDisplay = self.xlib.XOpenDisplay
        XOpenDisplay.restype = ctypes.POINTER(Display)
        XOpenDisplay.argtypes = [ctypes.c_char_p]

        if not self.display:
            self.display = self.xlib.XOpenDisplay(display)  # (display) or (None)

    def argbdata_to_pixdata(self, data, len):
        if data == None or len < 1: return None

        # Create byte array
        b = array.array('b', b'\x00' * 4 * len)

        offset, i = 0, 0
        while i < len:
            argb = data[i] & 0xffffffff
            rgba = (argb << 8) | (argb >> 24)
            b1 = (rgba >> 24) & 0xff
            b2 = (rgba >> 16) & 0xff
            b3 = (rgba >> 8) & 0xff
            b4 = rgba & 0xff

            struct.pack_into("=BBBB", b, offset, b1, b2, b3, b4)
            offset = offset + 4
            i = i + 1

        return b

    def getCursorImageData(self):
        # Call the function. Read data of cursor/mouse-pointer.
        cursor_data = self.XFixesGetCursorImage(self.display)

        if not (cursor_data and cursor_data[0]):
            raise Exception("Cannot read XFixesGetCursorImage()")

        # Note: cursor_data is a pointer, take cursor_data[0]
        return cursor_data[0]

    def getCursorImageArray(self):
        data = self.getCursorImageData()
        # x, y = data.x, data.y
        height, width = data.height, data.width

        bytearr = self.argbdata_to_pixdata(data.pixels, height * width)

        imgarray = np.array(bytearr, dtype=np.uint8)
        imgarray = imgarray.reshape(height, width, 4)
        del bytearr

        return imgarray

    def getCursorImageArrayFast(self):
        data = self.getCursorImageData()
        # x, y = data.x, data.y
        height, width = data.height, data.width

        bytearr = ctypes.cast(data.pixels, ctypes.POINTER(ctypes.c_ulong * height * width))[0]
        imgarray = np.array(bytearray(bytearr))
        imgarray = imgarray.reshape(height, width, 8)[:, :, (0, 1, 2, 3)]
        del bytearr

        return imgarray

    def saveImage(self, imgarray, text):
        from PIL import Image
        img = Image.fromarray(imgarray)
        img.save(text)


if __name__ == "__main__":
    cursor = Xcursor()
    imgarray = cursor.getCursorImageArrayFast()
    cursor.saveImage(imgarray, 'cursor_image.png')

```

## desktop_env/server/README.md

```markdown
<!-- vimc: call SyntaxRange#Include('```xml', '```', 'xml', 'NonText'): -->
<!-- vimc: call SyntaxRange#Include('```css', '```', 'css', 'NonText'): -->
<!-- vimc: call SyntaxRange#Include('```sh', '```', 'sh', 'NonText'): -->
<!-- vimc: call SyntaxRange#Include('```bash', '```', 'sh', 'NonText'): -->

### About the Converted Accessibility Tree

For several applications like Firefox or Thunderbird, you should first enable

	```sh
	gsettings set org.gnome.desktop.interface toolkit-accessibility true
	```

to see their accessibility tree.

#### Example of AT

An example of a node:

	```xml
	<section xmlns:attr="uri:deskat:attributes.at-spi.gnome.org" attr:class="subject" st:enabled="true" cp:screencoord="(1525, 169)", cp:windowcoord="(342, 162)", cp:size="(327, 21)">
	    歡迎使用新的 Outlook.com 帳戶
	</section>
	```

An example of a tree:

	```xml
	<desktop-frame ...>
	    <application name="Thunderbird" ...>
	        ... <!-- nodes of windows -->
	    </application>
	    ...
	</desktop-frame>
	```

#### Useful attributes

1. `name` - shows the name of application, title of window, or name of some
   component
2. `attr:class` - somewhat the same role as `class` in HTML
3. `attr:id` - somewhat the same role as `id` in HTML
4. `cp:screencoord` - absolute coordinator on the screen
5. `cp:windowcoord` - relative coordinator in the window
6. `cp:size` - the size

Also several states like `st:enabled` and `st:visible` can be indicated. A full
state list is available at
<https://gitlab.gnome.org/GNOME/pyatspi2/-/blob/master/pyatspi/state.py?ref_type=heads>.

#### How to use it in evaluation

See example `thunderbird/12086550-11c0-466b-b367-1d9e75b3910e.json` and
function `check_accessibility_tree` in `metrics/general.py`. You can use CSS
selector or XPath to reference a target nodes. You can also check its text
contents.

An example of a CSS selector:

	```css
	application[name=Thunderbird] page-tab-list[attr|id="tabmail-tabs"]>page-tab[name="About Profiles"]
	```

This selector will select the page tab of profile manager in Thunderbird (if open).

For usage of CSS selector: <https://www.w3.org/TR/selectors-3/>. For usage of XPath: <https://www.w3.org/TR/xpath-31/>.

#### Manual check

You can use accerciser to check the accessibility tree on GNOME VM.

	```sh
	sudo apt install accerciser
	```


### Additional Installation
Activating the window manager control requires the installation of `wmctrl`:
	```bash
	sudo apt install wmctrl
	```

To enable recording in the virtual machine, you need to install `ffmpeg`:
	```bash
	sudo apt install ffmpeg
	```

```

## evaluation_examples/README.md

```markdown
# Evaluation examples

Here we put the data examples to benchmark the ability of agents when interacting with GUI.
The examples are stored in `./examples` where each data item formatted as:

	```
	{
	    "id": "uid", # unique id
	    "snapshot": "snapshot_id", # the snapshot id of the environment, with some data already there and apps already opened, or just desktop
	    "instruction": "natural_language_instruction", # the natural language instruction of the task, what we want the agent to do
	    "source": "website_url", # where we know this example, some forum, or some website, or some paper
	    "config": {xxx}, # the scripts to setup the donwload and open files actions, as the initial state of a task
	    "trajectory": "trajectory_directory", # the trajectory directory, which contains the action sequence file, the screenshots and the recording video
	    "related_apps": ["app1", "app2", ...], # the related apps, which are opened during the task
	    "evaluator": "evaluation_dir", # the directory of the evaluator, which contains the evaluation script for this example
	…
	}
	```

The `./trajectories` file contains the annotated trajectories for each data item in `./examples` for finishing the task.

For now, it is under construction, and only tested on Windows 10. Please:
- Modify the path accordingly to run the evaluation;
- Remind us if some parts are overfit to our environment.

```

## evaluation_examples/test_all.json

```json
{
  "chrome": [
    "bb5e4c0d-f964-439c-97b6-bdb9747de3f4",
    "7b6c7e24-c58a-49fc-a5bb-d57b80e5b4c3",
    "06fe7178-4491-4589-810f-2e2bc9502122",
    "e1e75309-3ddb-4d09-92ec-de869c928143",
    "35253b65-1c19-4304-8aa4-6884b8218fc0",
    "2ad9387a-65d8-4e33-ad5b-7580065a27ca",
    "7a5a7856-f1b6-42a4-ade9-1ca81ca0f263",
    "44ee5668-ecd5-4366-a6ce-c1c9b8d4e938",
    "2ae9ba84-3a0d-4d4c-8338-3a1478dc5fe3",
    "480bcfea-d68f-4aaa-a0a9-2589ef319381",
    "af630914-714e-4a24-a7bb-f9af687d3b91",
    "3720f614-37fd-4d04-8a6b-76f54f8c222d",
    "99146c54-4f37-4ab8-9327-5f3291665e1e",
    "12086550-11c0-466b-b367-1d9e75b3910e",
    "6766f2b8-8a72-417f-a9e5-56fcaa735837",
    "93eabf48-6a27-4cb6-b963-7d5fe1e0d3a9",
    "ae78f875-5b98-4907-bbb5-9c737fc68c03",
    "3299584d-8f11-4457-bf4c-ce98f7600250",
    "030eeff7-b492-4218-b312-701ec99ee0cc",
    "9656a811-9b5b-4ddf-99c7-5117bcef0626",
    "fc6d8143-9452-4171-9459-7f515143419a",
    "a96b564e-dbe9-42c3-9ccf-b4498073438a",
    "1704f00f-79e6-43a7-961b-cedd3724d5fd",
    "f3b19d1e-2d48-44e9-b4e1-defcae1a0197",
    "82bc8d6a-36eb-4d2d-8801-ef714fb1e55a",
    "47543840-672a-467d-80df-8f7c3b9788c9",
    "c1fa57f3-c3db-4596-8f09-020701085416",
    "da46d875-6b82-4681-9284-653b0c7ae241",
    "6c4c23a1-42a4-43cc-9db1-2f86ff3738cc",
    "f79439ad-3ee8-4f99-a518-0eb60e5652b0",
    "b7895e80-f4d1-4648-bee0-4eb45a6f1fa8",
    "9f3f70fc-5afc-4958-a7b7-3bb4fcb01805",
    "7f52cab9-535c-4835-ac8c-391ee64dc930",
    "82279c77-8fc6-46f6-9622-3ba96f61b477",
    "2888b4e6-5b47-4b57-8bf5-c73827890774",
    "b4f95342-463e-4179-8c3f-193cd7241fb2",
    "f5d96daf-83a8-4c86-9686-bada31fc66ab",
    "121ba48f-9e17-48ce-9bc6-a4fb17a7ebba",
    "368d9ba4-203c-40c1-9fa3-da2f1430ce63",
    "59155008-fe71-45ec-8a8f-dc35497b6aa8",
    "a728a36e-8bf1-4bb6-9a03-ef039a5233f0",
    "b070486d-e161-459b-aa2b-ef442d973b92",
    "0d8b7de3-e8de-4d86-b9fd-dd2dce58a217",
    "9f935cce-0a9f-435f-8007-817732bfc0a5",
    "f0b971a1-6831-4b9b-a50e-22a6e47f45ba",
    "cabb3bae-cccb-41bd-9f5d-0f3a9fecd825"
  ],
  "gimp": [
    "7a4deb26-d57d-4ea9-9a73-630f66a7b568",
    "554785e9-4523-4e7a-b8e1-8016f565f56a",
    "77b8ab4d-994f-43ac-8930-8ca087d7c4b4",
    "f4aec372-4fb0-4df5-a52b-79e0e2a5d6ce",
    "d52d6308-ec58-42b7-a2c9-de80e4837b2b",
    "2a729ded-3296-423d-aec4-7dd55ed5fbb3",
    "b148e375-fe0b-4bec-90e7-38632b0d73c2",
    "a746add2-cab0-4740-ac36-c3769d9bfb46",
    "7b7617bd-57cc-468e-9c91-40c4ec2bcb3d",
    "d16c99dc-2a1e-46f2-b350-d97c86c85c15",
    "06ca5602-62ca-47f6-ad4f-da151cde54cc",
    "e2dd0213-26db-4349-abe5-d5667bfd725c",
    "f723c744-e62c-4ae6-98d1-750d3cd7d79d",
    "72f83cdc-bf76-4531-9a1b-eb893a13f8aa",
    "7767eef2-56a3-4cea-8c9f-48c070c7d65b",
    "734d6579-c07d-47a8-9ae2-13339795476b",
    "e19bd559-633b-4b02-940f-d946248f088e",
    "38f48d40-764e-4e77-a7cf-51dfce880291",
    "fbb548ca-c2a6-4601-9204-e39a2efc507b",
    "5ca86c6f-f317-49d8-b6a7-b527541caae8",
    "62f7fd55-0687-4a43-b6e1-3eda16fc6252",
    "8ea73f6f-9689-42ad-8c60-195bbf06a7ba",
    "58d3eeeb-e9d0-499f-962e-fd0db2a744d8",
    "2e6f678f-472d-4c55-99cc-8e7c5c402a71",
    "045bf3ff-9077-4b86-b483-a1040a949cff",
    "dbbf4b99-2253-4b10-9274-45f246af2466"
  ],
  "libreoffice_calc": [
    "357ef137-7eeb-4c80-a3bb-0951f26a8aff",
    "42e0a640-4f19-4b28-973d-729602b5a4a7",
    "51719eea-10bc-4246-a428-ac7c433dd4b3",
    "1954cced-e748-45c4-9c26-9855b97fbc5e",
    "2bd59342-0664-4ccb-ba87-79379096cc08",
    "3aaa4e37-dc91-482e-99af-132a612d40f3",
    "1273e544-688f-496b-8d89-3e0f40aa0606",
    "12382c62-0cd1-4bf2-bdc8-1d20bf9b2371",
    "f9584479-3d0d-4c79-affa-9ad7afdd8850",
    "535364ea-05bd-46ea-9937-9f55c68507e8",
    "7e429b8d-a3f0-4ed0-9b58-08957d00b127",
    "4f07fbe9-70de-4927-a4d5-bb28bc12c52c",
    "04d9aeaf-7bed-4024-bedb-e10e6f00eb7f",
    "0bf05a7d-b28b-44d2-955a-50b41e24012a",
    "6054afcb-5bab-4702-90a0-b259b5d3217c",
    "abed40dc-063f-4598-8ba5-9fe749c0615d",
    "37608790-6147-45d0-9f20-1137bb35703d",
    "26a8440e-c166-4c50-aef4-bfb77314b46b",
    "d681960f-7bc3-4286-9913-a8812ba3261a",
    "035f41ba-6653-43ab-aa63-c86d449d62e5",
    "7efeb4b1-3d19-4762-b163-63328d66303b",
    "1de60575-bb6e-4c3d-9e6a-2fa699f9f197",
    "aa3a8974-2e85-438b-b29e-a64df44deb4b",
    "51b11269-2ca8-4b2a-9163-f21758420e78",
    "1e8df695-bd1b-45b3-b557-e7d599cf7597",
    "ecb0df7a-4e8d-4a03-b162-053391d3afaf",
    "8b1ce5f2-59d2-4dcc-b0b0-666a714b9a14",
    "a01fbce3-2793-461f-ab86-43680ccbae25",
    "0326d92d-d218-48a8-9ca1-981cd6d064c7",
    "0a2e43bf-b26c-4631-a966-af9dfa12c9e5",
    "4188d3a4-077d-46b7-9c86-23e1a036f6c1",
    "347ef137-7eeb-4c80-a3bb-0951f26a8aff",
    "eb03d19a-b88d-4de4-8a64-ca0ac66f426b",
    "0cecd4f3-74de-457b-ba94-29ad6b5dafb6",
    "1d17d234-e39d-4ed7-b46f-4417922a4e7c",
    "4e6fcf72-daf3-439f-a232-c434ce416af6",
    "01b269ae-2111-4a07-81fd-3fcd711993b0",
    "21df9241-f8d7-4509-b7f1-37e501a823f7",
    "a9f325aa-8c05-4e4f-8341-9e4358565f4f",
    "6e99a1ad-07d2-4b66-a1ce-ece6d99c20a5",
    "7a4e4bc8-922c-4c84-865c-25ba34136be1",
    "4de54231-e4b5-49e3-b2ba-61a0bec721c0",
    "30e3e107-1cfb-46ee-a755-2cd080d7ba6a",
    "4172ea6e-6b77-4edb-a9cc-c0014bd1603b",
    "1334ca3e-f9e3-4db8-9ca7-b4c653be7d17",
    "3a7c8185-25c1-4941-bd7b-96e823c9f21f",
    "21ab7b40-77c2-4ae6-8321-e00d3a086c73"
  ],
  "libreoffice_impress": [
    "5d901039-a89c-4bfb-967b-bf66f4df075e",
    "550ce7e7-747b-495f-b122-acdc4d0b8e54",
    "455d3c66-7dc6-4537-a39a-36d3e9119df7",
    "af23762e-2bfd-4a1d-aada-20fa8de9ce07",
    "c59742c0-4323-4b9d-8a02-723c251deaa0",
    "ef9d12bd-bcee-4ba0-a40e-918400f43ddf",
    "9ec204e4-f0a3-42f8-8458-b772a6797cab",
    "0f84bef9-9790-432e-92b7-eece357603fb",
    "ce88f674-ab7a-43da-9201-468d38539e4a",
    "3b27600c-3668-4abd-8f84-7bcdebbccbdb",
    "a097acff-6266-4291-9fbd-137af7ecd439",
    "bf4e9888-f10f-47af-8dba-76413038b73c",
    "21760ecb-8f62-40d2-8d85-0cee5725cb72",
    "ac9bb6cb-1888-43ab-81e4-a98a547918cd",
    "2cd43775-7085-45d8-89fa-9e35c0a915cf",
    "358aa0a7-6677-453f-ae35-e440f004c31e",
    "a669ef01-ded5-4099-9ea9-25e99b569840",
    "73c99fb9-f828-43ce-b87a-01dc07faa224",
    "15aece23-a215-4579-91b4-69eec72e18da",
    "986fc832-6af2-417c-8845-9272b3a1528b",
    "a434992a-89df-4577-925c-0c58b747f0f4",
    "7dbc52a6-11e0-4c9a-a2cb-1e36cfda80d8",
    "841b50aa-df53-47bd-a73a-22d3a9f73160",
    "8979838c-54a5-4454-a2b8-3d135a1a5c8f",
    "b8adbc24-cef2-4b15-99d5-ecbe7ff445eb",
    "2b94c692-6abb-48ae-ab0b-b3e8a19cb340",
    "9cf05d24-6bd9-4dae-8967-f67d88f5d38a",
    "08aced46-45a2-48d7-993b-ed3fb5b32302",
    "edb61b14-a854-4bf5-a075-c8075c11293a",
    "c82632a4-56b6-4db4-9dd1-3820ee3388e4",
    "39be0d19-634d-4475-8768-09c130f5425d",
    "ac1b39ff-ee4d-4483-abce-c117e98942f0",
    "f23acfd2-c485-4b7c-a1e7-d4303ddfe864",
    "70bca0cc-c117-427e-b0be-4df7299ebeb6",
    "af2d657a-e6b3-4c6a-9f67-9e3ed015974c",
    "57667013-ea97-417c-9dce-2713091e6e2a",
    "0a211154-fda0-48d0-9274-eaac4ce5486d",
    "a53f80cd-4a90-4490-8310-097b011433f6",
    "7ae48c60-f143-4119-b659-15b8f485eb9a",
    "5cfb9197-e72b-454b-900e-c06b0c802b40",
    "05dd4c1d-c489-4c85-8389-a7836c4f0567",
    "5c1a6c3d-c1b3-47cb-9b01-8d1b7544ffa1",
    "4ed5abd0-8b5d-47bd-839f-cacfa15ca37a",
    "e4ef0baf-4b52-4590-a47e-d4d464cca2d7",
    "ed43c15f-00cb-4054-9c95-62c880865d68",
    "3161d64e-3120-47b4-aaad-6a764a92493b",
    "04578141-1d42-4146-b9cf-6fab4ce5fd74"
  ],
  "libreoffice_writer": [
    "0810415c-bde4-4443-9047-d5f70165a697",
    "0a0faba3-5580-44df-965d-f562a99b291c",
    "0b17a146-2934-46c7-8727-73ff6b6483e8",
    "0e47de2a-32e0-456c-a366-8c607ef7a9d2",
    "0e763496-b6bb-4508-a427-fad0b6c3e195",
    "3ef2b351-8a84-4ff2-8724-d86eae9b842e",
    "4bcb1253-a636-4df4-8cb0-a35c04dfef31",
    "66399b0d-8fda-4618-95c4-bfc6191617e9",
    "6a33f9b9-0a56-4844-9c3f-96ec3ffb3ba2",
    "6ada715d-3aae-4a32-a6a7-429b2e43fb93",
    "6f81754e-285d-4ce0-b59e-af7edb02d108",
    "72b810ef-4156-4d09-8f08-a0cf57e7cefe",
    "8472fece-c7dd-4241-8d65-9b3cd1a0b568",
    "88fe4b2d-3040-4c70-9a70-546a47764b48",
    "936321ce-5236-426a-9a20-e0e3c5dc536f",
    "adf5e2c3-64c7-4644-b7b6-d2f0167927e7",
    "b21acd93-60fd-4127-8a43-2f5178f4a830",
    "d53ff5ee-3b1a-431e-b2be-30ed2673079b",
    "e246f6d8-78d7-44ac-b668-fcf47946cb50",
    "e528b65e-1107-4b8c-8988-490e4fece599",
    "ecc2413d-8a48-416e-a3a2-d30106ca36cb",
    "f178a4a9-d090-4b56-bc4c-4b72a61a035d",
    "bb8ccc78-479f-4a2f-a71e-d565e439436b"
  ],
  "multi_apps": [
    "2b9493d7-49b8-493a-a71b-56cd1f4d6908",
    "2c9fc0de-3ee7-45e1-a5df-c86206ad78b5",
    "2fe4b718-3bd7-46ec-bdce-b184f5653624",
    "3680a5ee-6870-426a-a997-eba929a0d25c",
    "46407397-a7d5-4c6b-92c6-dbe038b1457b",
    "4e9f0faf-2ecc-4ae8-a804-28c9a75d1ddc",
    "510f64c8-9bcc-4be1-8d30-638705850618",
    "51f5801c-18b3-4f25-b0c3-02f85507a078",
    "58565672-7bfe-48ab-b828-db349231de6b",
    "78aed49a-a710-4321-a793-b611a7c5b56b",
    "897e3b53-5d4d-444b-85cb-2cdc8a97d903",
    "937087b6-f668-4ba6-9110-60682ee33441",
    "a0b9dc9c-fc07-4a88-8c5d-5e3ecad91bcb",
    "b52b40a5-ad70-4c53-b5b0-5650a8387052",
    "c867c42d-a52d-4a24-8ae3-f75d256b5618",
    "d9b7c649-c975-4f53-88f5-940b29c47247",
    "e135df7c-7687-4ac0-a5f0-76b74438b53e",
    "ee9a3c83-f437-4879-8918-be5efbb9fac7",
    "f7dfbef3-7697-431c-883a-db8583a4e4f9",
    "f8cfa149-d1c1-4215-8dac-4a0932bad3c2",
    "6d72aad6-187a-4392-a4c4-ed87269c51cf",
    "f918266a-b3e0-4914-865d-4faa564f1aef",
    "da52d699-e8d2-4dc5-9191-a2199e0b6a9b",
    "bc2b57f3-686d-4ec9-87ce-edf850b7e442",
    "74d5859f-ed66-4d3e-aa0e-93d7a592ce41",
    "b5062e3e-641c-4e3a-907b-ac864d2e7652",
    "00fa164e-2612-4439-992e-157d019a8436",
    "acb0f96b-e27c-44d8-b55f-7cb76609dfcd",
    "69acbb55-d945-4927-a87b-8480e1a5bb7e",
    "48d05431-6cd5-4e76-82eb-12b60d823f7d",
    "68a25bd4-59c7-4f4d-975e-da0c8509c848",
    "eb303e01-261e-4972-8c07-c9b4e7a4922a",
    "0c825995-5b70-4526-b663-113f4c999dd2",
    "c7c1e4c3-9e92-4eba-a4b8-689953975ea4",
    "d1acdb87-bb67-4f30-84aa-990e56a09c92",
    "deec51c9-3b1e-4b9e-993c-4776f20e8bb2",
    "8e116af7-7db7-4e35-a68b-b0939c066c78",
    "337d318b-aa07-4f4f-b763-89d9a2dd013f",
    "82e3c869-49f6-4305-a7ce-f3e64a0618e7",
    "185f29bd-5da0-40a6-b69c-ba7f4e0324ef",
    "869de13e-bef9-4b91-ba51-f6708c40b096",
    "2c1ebcd7-9c6d-4c9a-afad-900e381ecd5e",
    "3a93cae4-ad3e-403e-8c12-65303b271818",
    "1f18aa87-af6f-41ef-9853-cdb8f32ebdea",
    "26150609-0da3-4a7d-8868-0faf9c5f01bb",
    "9219480b-3aed-47fc-8bac-d2cffc5849f7",
    "881deb30-9549-4583-a841-8270c65f2a17",
    "7e287123-70ca-47b9-8521-47db09b69b14",
    "e2392362-125e-4f76-a2ee-524b183a3412",
    "5bc63fb9-276a-4439-a7c1-9dc76401737f",
    "26660ad1-6ebb-4f59-8cba-a8432dfe8d38",
    "a82b78bb-7fde-4cb3-94a4-035baf10bcf0",
    "36037439-2044-4b50-b9d1-875b5a332143",
    "716a6079-22da-47f1-ba73-c9d58f986a38",
    "873cafdd-a581-47f6-8b33-b9696ddb7b05",
    "a74b607e-6bb5-4ea8-8a7c-5d97c7bbcd2a",
    "6f4073b8-d8ea-4ade-8a18-c5d1d5d5aa9a",
    "da922383-bfa4-4cd3-bbad-6bebab3d7742",
    "2373b66a-092d-44cb-bfd7-82e86e7a3b4d",
    "81c425f5-78f3-4771-afd6-3d2973825947",
    "bb83cab4-e5c7-42c7-a67b-e46068032b86",
    "227d2f97-562b-4ccb-ae47-a5ec9e142fbb",
    "b337d106-053f-4d37-8da0-7f9c4043a66b",
    "20236825-b5df-46e7-89bf-62e1d640a897",
    "8df7e444-8e06-4f93-8a1a-c5c974269d82",
    "aad10cd7-9337-4b62-b704-a857848cedf2",
    "02ce9a50-7af2-47ed-8596-af0c230501f8",
    "4c26e3f3-3a14-4d86-b44a-d3cedebbb487",
    "a503b07f-9119-456b-b75d-f5146737d24f",
    "09a37c51-e625-49f4-a514-20a773797a8a",
    "3e3fc409-bff3-4905-bf16-c968eee3f807",
    "f5c13cdd-205c-4719-a562-348ae5cd1d91",
    "5990457f-2adb-467b-a4af-5c857c92d762",
    "415ef462-bed3-493a-ac36-ca8c6d23bf1b",
    "7ff48d5b-2df2-49da-b500-a5150ffc7f18",
    "9f3bb592-209d-43bc-bb47-d77d9df56504",
    "dd60633f-2c72-42ba-8547-6f2c8cb0fdb0",
    "ce2b64a2-ddc1-4f91-8c7d-a88be7121aac",
    "3f05f3b9-29ba-4b6b-95aa-2204697ffc06",
    "e1fc0df3-c8b9-4ee7-864c-d0b590d3aa56",
    "f8369178-fafe-40c2-adc4-b9b08a125456",
    "778efd0a-153f-4842-9214-f05fc176b877",
    "47f7c0ce-a5fb-4100-a5e6-65cd0e7429e5",
    "c2751594-0cd5-4088-be1b-b5f2f9ec97c4",
    "788b3701-3ec9-4b67-b679-418bfa726c22",
    "48c46dc7-fe04-4505-ade7-723cba1aa6f6",
    "42d25c08-fb87-4927-8b65-93631280a26f",
    "e8172110-ec08-421b-a6f5-842e6451911f",
    "42f4d1c7-4521-4161-b646-0a8934e36081",
    "3c8f201a-009d-4bbe-8b65-a6f8b35bb57f",
    "d68204bf-11c1-4b13-b48b-d303c73d4bf6",
    "91190194-f406-4cd6-b3f9-c43fac942b22",
    "7f35355e-02a6-45b5-b140-f0be698bcf85",
    "98e8e339-5f91-4ed2-b2b2-12647cb134f4",
    "0e5303d4-8820-42f6-b18d-daf7e633de21",
    "df67aebb-fb3a-44fd-b75b-51b6012df509",
    "5df7b33a-9f77-4101-823e-02f863e1c1ae",
    "aceb0368-56b8-4073-b70e-3dc9aee184e0",
    "22a4636f-8179-4357-8e87-d1743ece1f81",
    "236833a3-5704-47fc-888c-4f298f09f799",
    "67890eb6-6ce5-4c00-9e3d-fb4972699b06"
  ],
  "os": [
    "94d95f96-9699-4208-98ba-3c3119edf9c2",
    "bedcedc4-4d72-425e-ad62-21960b11fe0d",
    "ec4e3f68-9ea4-4c18-a5c9-69f89d1178b3",
    "a462a795-fdc7-4b23-b689-e8b6df786b78",
    "f9be0997-4b7c-45c5-b05c-4612b44a6118",
    "28cc3b7e-b194-4bc9-8353-d04c0f4d56d2",
    "5ea617a3-0e86-4ba6-aab2-dac9aa2e8d57",
    "e0df059f-28a6-4169-924f-b9623e7184cc",
    "b6781586-6346-41cd-935a-a6b1487918fc",
    "b3d4a89c-53f2-4d6b-8b6a-541fb5d205fa",
    "3ce045a0-877b-42aa-8d2c-b4a863336ab8",
    "fe41f596-a71b-4c2f-9b2f-9dcd40b568c3",
    "a4d98375-215b-4a4d-aee9-3d4370fccc41",
    "13584542-872b-42d8-b299-866967b5c3ef",
    "23393935-50c7-4a86-aeea-2b78fd089c5c",
    "5812b315-e7bd-4265-b51f-863c02174c28",
    "c288e301-e626-4b98-a1ab-159dcb162af5",
    "4783cc41-c03c-4e1b-89b4-50658f642bd5",
    "5c1075ca-bb34-46a3-a7a0-029bd7463e79",
    "5ced85fc-fa1a-4217-95fd-0fb530545ce2",
    "37887e8c-da15-4192-923c-08fa390a176d",
    "4127319a-8b79-4410-b58a-7a151e15f3d7",
    "4d117223-a354-47fb-8b45-62ab1390a95f",
    "6f56bf42-85b8-4fbb-8e06-6c44960184ba"
  ],
  "thunderbird": [
    "bb5e4c0d-f964-439c-97b6-bdb9747de3f4",
    "7b6c7e24-c58a-49fc-a5bb-d57b80e5b4c3",
    "12086550-11c0-466b-b367-1d9e75b3910e",
    "06fe7178-4491-4589-810f-2e2bc9502122",
    "6766f2b8-8a72-417f-a9e5-56fcaa735837",
    "e1e75309-3ddb-4d09-92ec-de869c928143",
    "3d1682a7-0fb0-49ae-a4dc-a73afd2d06d5",
    "35253b65-1c19-4304-8aa4-6884b8218fc0",
    "d088f539-cab4-4f9a-ac92-9999fc3a656e",
    "2ad9387a-65d8-4e33-ad5b-7580065a27ca",
    "480bcfea-d68f-4aaa-a0a9-2589ef319381",
    "030eeff7-b492-4218-b312-701ec99ee0cc",
    "94760984-3ff5-41ee-8347-cf1af709fea0",
    "99146c54-4f37-4ab8-9327-5f3291665e1e",
    "c9e7eaf2-b1a1-4efc-a982-721972fa9f02"
  ],
  "vlc": [
    "59f21cfb-0120-4326-b255-a5b827b38967",
    "8ba5ae7a-5ae5-4eab-9fcc-5dd4fe3abf89",
    "8f080098-ddb1-424c-b438-4e96e5e4786e",
    "bba3381f-b5eb-4439-bd9e-80c22218d5a7",
    "fba2c100-79e8-42df-ae74-b592418d54f4",
    "efcf0d81-0835-4880-b2fd-d866e8bc2294",
    "8d9fd4e2-6fdb-46b0-b9b9-02f06495c62f",
    "aa4b5023-aef6-4ed9-bdc9-705f59ab9ad6",
    "386dbd0e-0241-4a0a-b6a2-6704fba26b1c",
    "9195653c-f4aa-453d-aa95-787f6ccfaae9",
    "d06f0d4d-2cd5-4ede-8de9-598629438c6e",
    "a5bbbcd5-b398-4c91-83d4-55e1e31bbb81",
    "5ac2891a-eacd-4954-b339-98abba077adb",
    "f3977615-2b45-4ac5-8bba-80c17dbe2a37",
    "215dfd39-f493-4bc3-a027-8a97d72c61bf",
    "cb130f0d-d36f-4302-9838-b3baf46139b6",
    "7882ed6e-bece-4bf0-bada-c32dc1ddae72"
  ],
  "vs_code": [
    "0ed39f63-6049-43d4-ba4d-5fa2fe04a951",
    "53ad5833-3455-407b-bbc6-45b4c79ab8fb",
    "eabc805a-bfcf-4460-b250-ac92135819f6",
    "982d12a5-beab-424f-8d38-d2a48429e511",
    "4e60007a-f5be-4bfc-9723-c39affa0a6d3",
    "e2b5e914-ffe1-44d2-8e92-58f8c5d92bb2",
    "9439a27b-18ae-42d8-9778-5f68f891805e",
    "ea98c5d7-3cf9-4f9b-8ad3-366b58e0fcae",
    "930fdb3b-11a8-46fe-9bac-577332e2640e",
    "276cc624-87ea-4f08-ab93-f770e3790175",
    "9d425400-e9b2-4424-9a4b-d4c7abac4140",
    "5e2d93d8-8ad0-4435-b150-1692aacaa994",
    "6ed0a554-cbee-4b44-84ea-fd6c042f4fe1",
    "ec71221e-ac43-46f9-89b8-ee7d80f7e1c5",
    "70745df8-f2f5-42bd-8074-fbc10334fcc5",
    "57242fad-77ca-454f-b71b-f187181a9f23",
    "c6bf789c-ba3a-4209-971d-b63abf0ab733",
    "0512bb38-d531-4acf-9e7e-0add90816068",
    "847a96b6-df94-4927-97e6-8cc9ea66ced7",
    "7aeae0e2-70ee-4705-821d-1bba5d5b2ddd",
    "dcbe20e8-647f-4f1d-8696-f1c5bbb570e3",
    "7c4cc09e-7a92-40dd-8338-b2286535c4ed",
    "971cbb5b-3cbf-4ff7-9e24-b5c84fcebfa6"
  ]
}
```

## evaluation_examples/test_small.json

```json
{
  "chrome": [
    "bb5e4c0d-f964-439c-97b6-bdb9747de3f4",
    "7b6c7e24-c58a-49fc-a5bb-d57b80e5b4c3",
    "35253b65-1c19-4304-8aa4-6884b8218fc0",
    "a96b564e-dbe9-42c3-9ccf-b4498073438a"
  ],
  "gimp": [
    "7a4deb26-d57d-4ea9-9a73-630f66a7b568",
    "554785e9-4523-4e7a-b8e1-8016f565f56a"
  ],
  "libreoffice_calc": [
    "357ef137-7eeb-4c80-a3bb-0951f26a8aff",
    "42e0a640-4f19-4b28-973d-729602b5a4a7",
    "abed40dc-063f-4598-8ba5-9fe749c0615d"
  ],
  "libreoffice_impress": [
    "5d901039-a89c-4bfb-967b-bf66f4df075e",
    "550ce7e7-747b-495f-b122-acdc4d0b8e54"
  ],
  "libreoffice_writer": [
    "0810415c-bde4-4443-9047-d5f70165a697",
    "0a0faba3-5580-44df-965d-f562a99b291c"
  ],
  "multi_apps": [
    "a74b607e-6bb5-4ea8-8a7c-5d97c7bbcd2a",
    "5990457f-2adb-467b-a4af-5c857c92d762",
    "2b9493d7-49b8-493a-a71b-56cd1f4d6908",
    "46407397-a7d5-4c6b-92c6-dbe038b1457b",
    "4e9f0faf-2ecc-4ae8-a804-28c9a75d1ddc",
    "510f64c8-9bcc-4be1-8d30-638705850618",
    "897e3b53-5d4d-444b-85cb-2cdc8a97d903",
    "c867c42d-a52d-4a24-8ae3-f75d256b5618",
    "74d5859f-ed66-4d3e-aa0e-93d7a592ce41",
    "b5062e3e-641c-4e3a-907b-ac864d2e7652",
    "48d05431-6cd5-4e76-82eb-12b60d823f7d",
    "eb303e01-261e-4972-8c07-c9b4e7a4922a",
    "d1acdb87-bb67-4f30-84aa-990e56a09c92",
    "deec51c9-3b1e-4b9e-993c-4776f20e8bb2",
    "8e116af7-7db7-4e35-a68b-b0939c066c78",
    "716a6079-22da-47f1-ba73-c9d58f986a38",
    "2373b66a-092d-44cb-bfd7-82e86e7a3b4d"
  ],
  "os": [
    "5ea617a3-0e86-4ba6-aab2-dac9aa2e8d57",
    "5812b315-e7bd-4265-b51f-863c02174c28"
  ],
  "thunderbird": [
    "bb5e4c0d-f964-439c-97b6-bdb9747de3f4",
    "7b6c7e24-c58a-49fc-a5bb-d57b80e5b4c3"
  ],
  "vlc": [
    "59f21cfb-0120-4326-b255-a5b827b38967",
    "8f080098-ddb1-424c-b438-4e96e5e4786e"
  ],
  "vs_code": [
    "0ed39f63-6049-43d4-ba4d-5fa2fe04a951",
    "53ad5833-3455-407b-bbc6-45b4c79ab8fb",
    "276cc624-87ea-4f08-ab93-f770e3790175"
  ]
}
```

## evaluation_examples/examples/template.json

```json
{
  "id": "",
  "snapshot": "libreoffice_calc",
  "instruction": "",
  "source": "",
  "config": [
    {
      "type": "",
      "parameters": {}
    }
  ],
  "trajectory": "trajectories/",
  "related_apps": [
    "app1",
    "app2"
  ],
  "evaluator": {
    "postconfig": [],
    "func": "func",
    "result": {
      "type": ""
    },
    "expected": {
      "type": ""
    }
  }
}

```

## mm_agents/agent.py

```python
import base64
import json
import logging
import os
import re
import time
import uuid
import xml.etree.ElementTree as ET
from http import HTTPStatus
from io import BytesIO
from typing import Dict, List

import backoff
import dashscope
import google.generativeai as genai
import openai
import requests
import tiktoken
from PIL import Image
from google.api_core.exceptions import InvalidArgument

from mm_agents.accessibility_tree_wrap.heuristic_retrieve import filter_nodes, draw_bounding_boxes
from mm_agents.prompts import SYS_PROMPT_IN_SCREENSHOT_OUT_CODE, SYS_PROMPT_IN_SCREENSHOT_OUT_ACTION, \
    SYS_PROMPT_IN_A11Y_OUT_CODE, SYS_PROMPT_IN_A11Y_OUT_ACTION, \
    SYS_PROMPT_IN_BOTH_OUT_CODE, SYS_PROMPT_IN_BOTH_OUT_ACTION, \
    SYS_PROMPT_IN_SOM_OUT_TAG

logger = logging.getLogger("desktopenv.agent")


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def linearize_accessibility_tree(accessibility_tree, platform="ubuntu"):
    # leaf_nodes = find_leaf_nodes(accessibility_tree)
    filtered_nodes = filter_nodes(ET.fromstring(accessibility_tree), platform)

    linearized_accessibility_tree = ["tag\tname\ttext\tposition (top-left x&y)\tsize (w&h)"]
    # Linearize the accessibility tree nodes into a table format

    for node in filtered_nodes:
        # linearized_accessibility_tree += node.tag + "\t"
        # linearized_accessibility_tree += node.attrib.get('name') + "\t"
        if node.text:
            text = (node.text if '"' not in node.text \
                        else '"{:}"'.format(node.text.replace('"', '""'))
                    )
        elif node.get("{uri:deskat:uia.windows.microsoft.org}class", "").endswith("EditWrapper") \
                and node.get("{uri:deskat:value.at-spi.gnome.org}value"):
            text: str = node.get("{uri:deskat:value.at-spi.gnome.org}value")
            text = (text if '"' not in text \
                        else '"{:}"'.format(text.replace('"', '""'))
                    )
        else:
            text = '""'
        # linearized_accessibility_tree += node.attrib.get(
        # , "") + "\t"
        # linearized_accessibility_tree += node.attrib.get('{uri:deskat:component.at-spi.gnome.org}size', "") + "\n"
        linearized_accessibility_tree.append(
            "{:}\t{:}\t{:}\t{:}\t{:}".format(
                node.tag, node.get("name", ""), text
                , node.get('{uri:deskat:component.at-spi.gnome.org}screencoord', "")
                , node.get('{uri:deskat:component.at-spi.gnome.org}size', "")
            )
        )

    return "\n".join(linearized_accessibility_tree)


def tag_screenshot(screenshot, accessibility_tree, platform="ubuntu"):
    # Creat a tmp file to store the screenshot in random name
    uuid_str = str(uuid.uuid4())
    os.makedirs("tmp/images", exist_ok=True)
    tagged_screenshot_file_path = os.path.join("tmp/images", uuid_str + ".png")
    # nodes = filter_nodes(find_leaf_nodes(accessibility_tree))
    nodes = filter_nodes(ET.fromstring(accessibility_tree), platform=platform, check_image=True)
    # Make tag screenshot
    marks, drew_nodes, element_list = draw_bounding_boxes(nodes, screenshot, tagged_screenshot_file_path)

    return marks, drew_nodes, tagged_screenshot_file_path, element_list


def parse_actions_from_string(input_string):
    if input_string.strip() in ['WAIT', 'DONE', 'FAIL']:
        return [input_string.strip()]
    # Search for a JSON string within the input string
    actions = []
    matches = re.findall(r'```json\s+(.*?)\s+```', input_string, re.DOTALL)
    if matches:
        # Assuming there's only one match, parse the JSON string into a dictionary
        try:
            for match in matches:
                action_dict = json.loads(match)
                actions.append(action_dict)
            return actions
        except json.JSONDecodeError as e:
            return f"Failed to parse JSON: {e}"
    else:
        matches = re.findall(r'```\s+(.*?)\s+```', input_string, re.DOTALL)
        if matches:
            # Assuming there's only one match, parse the JSON string into a dictionary
            try:
                for match in matches:
                    action_dict = json.loads(match)
                    actions.append(action_dict)
                return actions
            except json.JSONDecodeError as e:
                return f"Failed to parse JSON: {e}"
        else:
            try:
                action_dict = json.loads(input_string)
                return [action_dict]
            except json.JSONDecodeError:
                raise ValueError("Invalid response format: " + input_string)


def parse_code_from_string(input_string):
    input_string = input_string.replace(";", "\n")
    if input_string.strip() in ['WAIT', 'DONE', 'FAIL']:
        return [input_string.strip()]

    # This regular expression will match both ```code``` and ```python code```
    # and capture the `code` part. It uses a non-greedy match for the content inside.
    pattern = r"```(?:\w+\s+)?(.*?)```"
    # Find all non-overlapping matches in the string
    matches = re.findall(pattern, input_string, re.DOTALL)

    # The regex above captures the content inside the triple backticks.
    # The `re.DOTALL` flag allows the dot `.` to match newline characters as well,
    # so the code inside backticks can span multiple lines.

    # matches now contains all the captured code snippets

    codes = []

    for match in matches:
        match = match.strip()
        commands = ['WAIT', 'DONE', 'FAIL']  # fixme: updates this part when we have more commands

        if match in commands:
            codes.append(match.strip())
        elif match.split('\n')[-1] in commands:
            if len(match.split('\n')) > 1:
                codes.append("\n".join(match.split('\n')[:-1]))
            codes.append(match.split('\n')[-1])
        else:
            codes.append(match)

    return codes


def parse_code_from_som_string(input_string, masks):
    # parse the output string by masks
    tag_vars = ""
    for i, mask in enumerate(masks):
        x, y, w, h = mask
        tag_vars += "tag_" + str(i + 1) + "=" + "({}, {})".format(int(x + w // 2), int(y + h // 2))
        tag_vars += "\n"

    actions = parse_code_from_string(input_string)

    for i, action in enumerate(actions):
        if action.strip() in ['WAIT', 'DONE', 'FAIL']:
            pass
        else:
            action = tag_vars + action
            actions[i] = action

    return actions


def trim_accessibility_tree(linearized_accessibility_tree, max_tokens):
    enc = tiktoken.encoding_for_model("gpt-4")
    tokens = enc.encode(linearized_accessibility_tree)
    if len(tokens) > max_tokens:
        linearized_accessibility_tree = enc.decode(tokens[:max_tokens])
        linearized_accessibility_tree += "[...]\n"
    return linearized_accessibility_tree


class PromptAgent:
    def __init__(
            self,
            platform="ubuntu",
            model="gpt-4-vision-preview",
            max_tokens=1500,
            top_p=0.9,
            temperature=0.5,
            action_space="computer_13",
            observation_type="screenshot_a11y_tree",
            # observation_type can be in ["screenshot", "a11y_tree", "screenshot_a11y_tree", "som"]
            max_trajectory_length=3,
            a11y_tree_max_tokens=10000
    ):
        self.platform = platform
        self.model = model
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.temperature = temperature
        self.action_space = action_space
        self.observation_type = observation_type
        self.max_trajectory_length = max_trajectory_length
        self.a11y_tree_max_tokens = a11y_tree_max_tokens

        self.thoughts = []
        self.actions = []
        self.observations = []

        if observation_type == "screenshot":
            if action_space == "computer_13":
                self.system_message = SYS_PROMPT_IN_SCREENSHOT_OUT_ACTION
            elif action_space == "pyautogui":
                self.system_message = SYS_PROMPT_IN_SCREENSHOT_OUT_CODE
            else:
                raise ValueError("Invalid action space: " + action_space)
        elif observation_type == "a11y_tree":
            if action_space == "computer_13":
                self.system_message = SYS_PROMPT_IN_A11Y_OUT_ACTION
            elif action_space == "pyautogui":
                self.system_message = SYS_PROMPT_IN_A11Y_OUT_CODE
            else:
                raise ValueError("Invalid action space: " + action_space)
        elif observation_type == "screenshot_a11y_tree":
            if action_space == "computer_13":
                self.system_message = SYS_PROMPT_IN_BOTH_OUT_ACTION
            elif action_space == "pyautogui":
                self.system_message = SYS_PROMPT_IN_BOTH_OUT_CODE
            else:
                raise ValueError("Invalid action space: " + action_space)
        elif observation_type == "som":
            if action_space == "computer_13":
                raise ValueError("Invalid action space: " + action_space)
            elif action_space == "pyautogui":
                self.system_message = SYS_PROMPT_IN_SOM_OUT_TAG
            else:
                raise ValueError("Invalid action space: " + action_space)
        else:
            raise ValueError("Invalid experiment type: " + observation_type)

    def predict(self, instruction: str, obs: Dict) -> List:
        """
        Predict the next action(s) based on the current observation.
        """
        system_message = self.system_message + "\nYou are asked to complete the following task: {}".format(instruction)

        # Prepare the payload for the API call
        messages = []
        masks = None

        messages.append({
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": system_message
                },
            ]
        })

        # Append trajectory
        assert len(self.observations) == len(self.actions) and len(self.actions) == len(self.thoughts) \
            , "The number of observations and actions should be the same."

        if len(self.observations) > self.max_trajectory_length:
            if self.max_trajectory_length == 0:
                _observations = []
                _actions = []
                _thoughts = []
            else:
                _observations = self.observations[-self.max_trajectory_length:]
                _actions = self.actions[-self.max_trajectory_length:]
                _thoughts = self.thoughts[-self.max_trajectory_length:]
        else:
            _observations = self.observations
            _actions = self.actions
            _thoughts = self.thoughts

        for previous_obs, previous_action, previous_thought in zip(_observations, _actions, _thoughts):

            # {{{1
            if self.observation_type == "screenshot_a11y_tree":
                _screenshot = previous_obs["screenshot"]
                _linearized_accessibility_tree = previous_obs["accessibility_tree"]

                messages.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Given the screenshot and info from accessibility tree as below:\n{}\nWhat's the next step that you will do to help with the task?".format(
                                _linearized_accessibility_tree)
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{_screenshot}",
                                "detail": "high"
                            }
                        }
                    ]
                })
            elif self.observation_type in ["som"]:
                _screenshot = previous_obs["screenshot"]

                messages.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Given the tagged screenshot as below. What's the next step that you will do to help with the task?"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{_screenshot}",
                                "detail": "high"
                            }
                        }
                    ]
                })
            elif self.observation_type == "screenshot":
                _screenshot = previous_obs["screenshot"]

                messages.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Given the screenshot as below. What's the next step that you will do to help with the task?"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{_screenshot}",
                                "detail": "high"
                            }
                        }
                    ]
                })
            elif self.observation_type == "a11y_tree":
                _linearized_accessibility_tree = previous_obs["accessibility_tree"]

                messages.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Given the info from accessibility tree as below:\n{}\nWhat's the next step that you will do to help with the task?".format(
                                _linearized_accessibility_tree)
                        }
                    ]
                })
            else:
                raise ValueError("Invalid observation_type type: " + self.observation_type)  # 1}}}

            messages.append({
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": previous_thought.strip() if len(previous_thought) > 0 else "No valid action"
                    },
                ]
            })

        # {{{1
        if self.observation_type in ["screenshot", "screenshot_a11y_tree"]:
            base64_image = encode_image(obs["screenshot"])
            linearized_accessibility_tree = linearize_accessibility_tree(accessibility_tree=obs["accessibility_tree"],
                                                                         platform=self.platform) if self.observation_type == "screenshot_a11y_tree" else None
            logger.debug("LINEAR AT: %s", linearized_accessibility_tree)

            if linearized_accessibility_tree:
                linearized_accessibility_tree = trim_accessibility_tree(linearized_accessibility_tree,
                                                                        self.a11y_tree_max_tokens)

            if self.observation_type == "screenshot_a11y_tree":
                self.observations.append({
                    "screenshot": base64_image,
                    "accessibility_tree": linearized_accessibility_tree
                })
            else:
                self.observations.append({
                    "screenshot": base64_image,
                    "accessibility_tree": None
                })

            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Given the screenshot as below. What's the next step that you will do to help with the task?"
                        if self.observation_type == "screenshot"
                        else "Given the screenshot and info from accessibility tree as below:\n{}\nWhat's the next step that you will do to help with the task?".format(
                            linearized_accessibility_tree)
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}",
                            "detail": "high"
                        }
                    }
                ]
            })
        elif self.observation_type == "a11y_tree":
            linearized_accessibility_tree = linearize_accessibility_tree(accessibility_tree=obs["accessibility_tree"],
                                                                         platform=self.platform)
            logger.debug("LINEAR AT: %s", linearized_accessibility_tree)

            if linearized_accessibility_tree:
                linearized_accessibility_tree = trim_accessibility_tree(linearized_accessibility_tree,
                                                                        self.a11y_tree_max_tokens)

            self.observations.append({
                "screenshot": None,
                "accessibility_tree": linearized_accessibility_tree
            })

            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Given the info from accessibility tree as below:\n{}\nWhat's the next step that you will do to help with the task?".format(
                            linearized_accessibility_tree)
                    }
                ]
            })
        elif self.observation_type == "som":
            # Add som to the screenshot
            masks, drew_nodes, tagged_screenshot, linearized_accessibility_tree = tag_screenshot(obs["screenshot"], obs[
                "accessibility_tree"], self.platform)
            base64_image = encode_image(tagged_screenshot)
            logger.debug("LINEAR AT: %s", linearized_accessibility_tree)

            if linearized_accessibility_tree:
                linearized_accessibility_tree = trim_accessibility_tree(linearized_accessibility_tree,
                                                                        self.a11y_tree_max_tokens)

            self.observations.append({
                "screenshot": base64_image,
                "accessibility_tree": linearized_accessibility_tree
            })

            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Given the tagged screenshot and info from accessibility tree as below:\n{}\nWhat's the next step that you will do to help with the task?".format(
                            linearized_accessibility_tree)
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}",
                            "detail": "high"
                        }
                    }
                ]
            })
        else:
            raise ValueError("Invalid observation_type type: " + self.observation_type)  # 1}}}

        # with open("messages.json", "w") as f:
        #     f.write(json.dumps(messages, indent=4))

        # logger.info("PROMPT: %s", messages)

        response = self.call_llm({
            "model": self.model,
            "messages": messages,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "temperature": self.temperature
        })

        logger.info("RESPONSE: %s", response)

        try:
            actions = self.parse_actions(response, masks)
            self.thoughts.append(response)
        except ValueError as e:
            print("Failed to parse action from response", e)
            actions = None
            self.thoughts.append("")

        return response, actions

    @backoff.on_exception(
        backoff.expo,
        # here you should add more model exceptions as you want,
        # but you are forbidden to add "Exception", that is, a common type of exception
        # because we want to catch this kind of Exception in the outside to ensure each example won't exceed the time limit
        (openai.RateLimitError,
         openai.BadRequestError,
         openai.InternalServerError,
         InvalidArgument),
        max_tries=5
    )
    def call_llm(self, payload):

        if self.model.startswith("gpt"):
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"
            }
            logger.info("Generating content with GPT model: %s", self.model)
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload
            )

            if response.status_code != 200:
                if response.json()['error']['code'] == "context_length_exceeded":
                    logger.error("Context length exceeded. Retrying with a smaller context.")
                    payload["messages"] = [payload["messages"][0]] + payload["messages"][-1:]
                    retry_response = requests.post(
                        "https://api.openai.com/v1/chat/completions",
                        headers=headers,
                        json=payload
                    )
                    if retry_response.status_code != 200:
                        logger.error(
                            "Failed to call LLM even after attempt on shortening the history: " + retry_response.text)
                        return ""

                logger.error("Failed to call LLM: " + response.text)
                time.sleep(5)
                return ""
            else:
                return response.json()['choices'][0]['message']['content']

        elif self.model.startswith("claude"):
            messages = payload["messages"]
            max_tokens = payload["max_tokens"]
            top_p = payload["top_p"]
            temperature = payload["temperature"]

            claude_messages = []

            for i, message in enumerate(messages):
                claude_message = {
                    "role": message["role"],
                    "content": []
                }
                assert len(message["content"]) in [1, 2], "One text, or one text with one image"
                for part in message["content"]:

                    if part['type'] == "image_url":
                        image_source = {}
                        image_source["type"] = "base64"
                        image_source["media_type"] = "image/png"
                        image_source["data"] = part['image_url']['url'].replace("data:image/png;base64,", "")
                        claude_message['content'].append({"type": "image", "source": image_source})

                    if part['type'] == "text":
                        claude_message['content'].append({"type": "text", "text": part['text']})

                claude_messages.append(claude_message)

            # the claude not support system message in our endpoint, so we concatenate it at the first user message
            if claude_messages[0]['role'] == "system":
                claude_system_message_item = claude_messages[0]['content'][0]
                claude_messages[1]['content'].insert(0, claude_system_message_item)
                claude_messages.pop(0)

            logger.debug("CLAUDE MESSAGE: %s", repr(claude_messages))

            headers = {
                "x-api-key": os.environ["ANTHROPIC_API_KEY"],
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            }

            payload = {
                "model": self.model,
                "max_tokens": max_tokens,
                "messages": claude_messages,
                "temperature": temperature,
                "top_p": top_p
            }

            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=payload
            )

            if response.status_code != 200:

                logger.error("Failed to call LLM: " + response.text)
                time.sleep(5)
                return ""
            else:
                return response.json()['content'][0]['text']

        elif self.model.startswith("mistral"):
            messages = payload["messages"]
            max_tokens = payload["max_tokens"]
            top_p = payload["top_p"]
            temperature = payload["temperature"]

            mistral_messages = []

            for i, message in enumerate(messages):
                mistral_message = {
                    "role": message["role"],
                    "content": ""
                }

                for part in message["content"]:
                    mistral_message['content'] = part['text'] if part['type'] == "text" else ""

                mistral_messages.append(mistral_message)

            from openai import OpenAI

            client = OpenAI(api_key=os.environ["TOGETHER_API_KEY"],
                            base_url='https://api.together.xyz',
                            )
            logger.info("Generating content with Mistral model: %s", self.model)

            flag = 0
            while True:
                try:
                    if flag > 20: break
                    response = client.chat.completions.create(
                        messages=mistral_messages,
                        model=self.model,
                        max_tokens=max_tokens,
                        top_p=top_p,
                        temperature=temperature
                    )
                    break
                except:
                    if flag == 0:
                        mistral_messages = [mistral_messages[0]] + mistral_messages[-1:]
                    else:
                        mistral_messages[-1]["content"] = ' '.join(mistral_messages[-1]["content"].split()[:-500])
                    flag = flag + 1

            try:
                return response.choices[0].message.content
            except Exception as e:
                print("Failed to call LLM: " + str(e))
                return ""

        elif self.model.startswith("THUDM"):
            # THUDM/cogagent-chat-hf
            messages = payload["messages"]
            max_tokens = payload["max_tokens"]
            top_p = payload["top_p"]
            temperature = payload["temperature"]

            cog_messages = []

            for i, message in enumerate(messages):
                cog_message = {
                    "role": message["role"],
                    "content": []
                }

                for part in message["content"]:
                    if part['type'] == "image_url":
                        cog_message['content'].append(
                            {"type": "image_url", "image_url": {"url": part['image_url']['url']}})

                    if part['type'] == "text":
                        cog_message['content'].append({"type": "text", "text": part['text']})

                cog_messages.append(cog_message)

            # the cogagent not support system message in our endpoint, so we concatenate it at the first user message
            if cog_messages[0]['role'] == "system":
                cog_system_message_item = cog_messages[0]['content'][0]
                cog_messages[1]['content'].insert(0, cog_system_message_item)
                cog_messages.pop(0)

            payload = {
                "model": self.model,
                "max_tokens": max_tokens,
                "messages": cog_messages,
                "temperature": temperature,
                "top_p": top_p
            }

            base_url = "http://127.0.0.1:8000"

            response = requests.post(f"{base_url}/v1/chat/completions", json=payload, stream=False)
            if response.status_code == 200:
                decoded_line = response.json()
                content = decoded_line.get("choices", [{}])[0].get("message", "").get("content", "")
                return content
            else:
                print("Failed to call LLM: ", response.status_code)
                return ""

        elif self.model.startswith("gemini"):
            def encoded_img_to_pil_img(data_str):
                base64_str = data_str.replace("data:image/png;base64,", "")
                image_data = base64.b64decode(base64_str)
                image = Image.open(BytesIO(image_data))

                return image

            messages = payload["messages"]
            max_tokens = payload["max_tokens"]
            top_p = payload["top_p"]
            temperature = payload["temperature"]

            gemini_messages = []
            for i, message in enumerate(messages):
                role_mapping = {
                    "assistant": "model",
                    "user": "user",
                    "system": "system"
                }
                gemini_message = {
                    "role": role_mapping[message["role"]],
                    "parts": []
                }
                assert len(message["content"]) in [1, 2], "One text, or one text with one image"

                # The gemini only support the last image as single image input
                if i == len(messages) - 1:
                    for part in message["content"]:
                        gemini_message['parts'].append(part['text']) if part['type'] == "text" \
                            else gemini_message['parts'].append(encoded_img_to_pil_img(part['image_url']['url']))
                else:
                    for part in message["content"]:
                        gemini_message['parts'].append(part['text']) if part['type'] == "text" else None

                gemini_messages.append(gemini_message)

            # the mistral not support system message in our endpoint, so we concatenate it at the first user message
            if gemini_messages[0]['role'] == "system":
                gemini_messages[1]['parts'][0] = gemini_messages[0]['parts'][0] + "\n" + gemini_messages[1]['parts'][0]
                gemini_messages.pop(0)

            # since the gemini-pro-vision donnot support multi-turn message
            if self.model == "gemini-pro-vision":
                message_history_str = ""
                for message in gemini_messages:
                    message_history_str += "<|" + message['role'] + "|>\n" + message['parts'][0] + "\n"
                gemini_messages = [{"role": "user", "parts": [message_history_str, gemini_messages[-1]['parts'][1]]}]
                # gemini_messages[-1]['parts'][1].save("output.png", "PNG")

            # print(gemini_messages)
            api_key = os.environ.get("GENAI_API_KEY")
            assert api_key is not None, "Please set the GENAI_API_KEY environment variable"
            genai.configure(api_key=api_key)
            logger.info("Generating content with Gemini model: %s", self.model)
            request_options = {"timeout": 120}
            gemini_model = genai.GenerativeModel(self.model)
            try:
                response = gemini_model.generate_content(
                    gemini_messages,
                    generation_config={
                        "candidate_count": 1,
                        "max_output_tokens": max_tokens,
                        "top_p": top_p,
                        "temperature": temperature
                    },
                    safety_settings={
                        "harassment": "block_none",
                        "hate": "block_none",
                        "sex": "block_none",
                        "danger": "block_none"
                    },
                    request_options=request_options
                )
                return response.text
            except Exception as e:
                logger.error("Meet exception when calling Gemini API, " + str(e.__class__.__name__) + str(e))
                logger.error(f"count_tokens: {gemini_model.count_tokens(gemini_messages)}")
                logger.error(f"generation_config: {max_tokens}, {top_p}, {temperature}")
                return ""
        elif self.model.startswith("qwen"):
            messages = payload["messages"]
            max_tokens = payload["max_tokens"]
            top_p = payload["top_p"]
            if payload["temperature"]:
                logger.warning("Qwen model does not support temperature parameter, it will be ignored.")

            qwen_messages = []

            for i, message in enumerate(messages):
                qwen_message = {
                    "role": message["role"],
                    "content": []
                }
                assert len(message["content"]) in [1, 2], "One text, or one text with one image"
                for part in message["content"]:
                    qwen_message['content'].append({"image": part['image_url']['url']}) if part[
                                                                                               'type'] == "image_url" else None
                    qwen_message['content'].append({"text": part['text']}) if part['type'] == "text" else None

                qwen_messages.append(qwen_message)

            response = dashscope.MultiModalConversation.call(
                model='qwen-vl-plus',
                messages=messages,
                max_length=max_tokens,
                top_p=top_p,
            )
            # The response status_code is HTTPStatus.OK indicate success,
            # otherwise indicate request is failed, you can get error code
            # and message from code and message.
            if response.status_code == HTTPStatus.OK:
                try:
                    return response.json()['output']['choices'][0]['message']['content']
                except Exception:
                    return ""
            else:
                print(response.code)  # The error code.
                print(response.message)  # The error message.
                return ""

        else:
            raise ValueError("Invalid model: " + self.model)

    def parse_actions(self, response: str, masks=None):

        if self.observation_type in ["screenshot", "a11y_tree", "screenshot_a11y_tree"]:
            # parse from the response
            if self.action_space == "computer_13":
                actions = parse_actions_from_string(response)
            elif self.action_space == "pyautogui":
                actions = parse_code_from_string(response)
            else:
                raise ValueError("Invalid action space: " + self.action_space)

            self.actions.append(actions)

            return actions
        elif self.observation_type in ["som"]:
            # parse from the response
            if self.action_space == "computer_13":
                raise ValueError("Invalid action space: " + self.action_space)
            elif self.action_space == "pyautogui":
                actions = parse_code_from_som_string(response, masks)
            else:
                raise ValueError("Invalid action space: " + self.action_space)

            self.actions.append(actions)

            return actions

    def reset(self):
        self.thoughts = []
        self.actions = []
        self.observations = []

```

## mm_agents/prompts.py

```python
SYS_PROMPT_IN_SCREENSHOT_OUT_CODE = """
You are an agent which follow my instruction and perform desktop computer tasks as instructed.
You have good knowledge of computer and good internet connection and assume your code will run on a computer for controlling the mouse and keyboard.
For each step, you will get an observation of an image, which is the screenshot of the computer screen and you will predict the action of the computer based on the image.

You are required to use `pyautogui` to perform the action grounded to the observation, but DONOT use the `pyautogui.locateCenterOnScreen` function to locate the element you want to operate with since we have no image of the element you want to operate with. DONOT USE `pyautogui.screenshot()` to make screenshot.
Return one line or multiple lines of python code to perform the action each time, be time efficient. When predicting multiple lines of code, make some small sleep like `time.sleep(0.5);` interval so that the machine could take; Each time you need to predict a complete code, no variables or function can be shared from history
You need to to specify the coordinates of by yourself based on your observation of current observation, but you should be careful to ensure that the coordinates are correct.
You ONLY need to return the code inside a code block, like this:
	```python
	# your code here
	```
Specially, it is also allowed to return the following special code:
When you think you have to wait for some time, return ```WAIT```;
When you think the task can not be done, return ```FAIL```, don't easily say ```FAIL```, try your best to do the task;
When you think the task is done, return ```DONE```.

My computer's password is 'password', feel free to use it when you need sudo rights.
First give the current screenshot and previous things we did a short reflection, then RETURN ME THE CODE OR SPECIAL CODE I ASKED FOR. NEVER EVER RETURN ME ANYTHING ELSE.
""".strip()

SYS_PROMPT_IN_SCREENSHOT_OUT_CODE_FEW_SHOT = """
You are an agent which follow my instruction and perform desktop computer tasks as instructed.
You have good knowledge of computer and good internet connection and assume your code will run on a computer for controlling the mouse and keyboard.
For each step, you will get an observation of an image, which is the screenshot of the computer screen and the instruction and you will predict the next action to operate on the computer based on the image.

You are required to use `pyautogui` to perform the action grounded to the observation, but DONOT use the `pyautogui.locateCenterOnScreen` function to locate the element you want to operate with since we have no image of the element you want to operate with. DONOT USE `pyautogui.screenshot()` to make screenshot.
Return one line or multiple lines of python code to perform the action each time, be time efficient. When predicting multiple lines of code, make some small sleep like `time.sleep(0.5);` interval so that the machine could take; Each time you need to predict a complete code, no variables or function can be shared from history
You need to to specify the coordinates of by yourself based on your observation of current observation, but you should be careful to ensure that the coordinates are correct.
You ONLY need to return the code inside a code block, like this:
	```python
	# your code here
	```
Specially, it is also allowed to return the following special code:
When you think you have to wait for some time, return ```WAIT```;
When you think the task can not be done, return ```FAIL```, don't easily say ```FAIL```, try your best to do the task;
When you think the task is done, return ```DONE```.

My computer's password is 'password', feel free to use it when you need sudo rights.
Our past communication is great, and what you have done is very helpful. I will now give you another task to complete.
First take a deep breath, think step by step, give the current screenshot a thinking, then RETURN ME THE CODE OR SPECIAL CODE I ASKED FOR. NEVER EVER RETURN ME ANYTHING ELSE.
""".strip()

SYS_PROMPT_IN_SCREENSHOT_OUT_ACTION = """
You will act as an agent which follow my instruction and perform desktop computer tasks as instructed. You must have good knowledge of computer and good internet connection.
For each step, you will get an observation of an image, which is the screenshot of the computer screen. And you will predict the action of the computer based on the image.

HERE is the description of the action space you need to predict, follow the format and choose the correct action type and parameters:
ACTION_SPACE = [
    {
        "action_type": "MOVE_TO",
        "note": "move the cursor to the specified position",
        "parameters": {
            "x": {
                "type": float,
                "range": [0, X_MAX],
                "optional": False,
            },
            "y": {
                "type": float,
                "range": [0, Y_MAX],
                "optional": False,
            }
        }
    },
    {
        "action_type": "CLICK",
        "note": "click the left button if the button not specified, otherwise click the specified button; click at the current position if x and y are not specified, otherwise click at the specified position",
        "parameters": {
            "button": {
                "type": str,
                "range": ["left", "right", "middle"],
                "optional": True,
            },
            "x": {
                "type": float,
                "range": [0, X_MAX],
                "optional": True,
            },
            "y": {
                "type": float,
                "range": [0, Y_MAX],
                "optional": True,
            },
            "num_clicks": {
                "type": int,
                "range": [1, 2, 3],
                "optional": True,
            },
        }
    },
    {
        "action_type": "MOUSE_DOWN",
        "note": "press the left button if the button not specified, otherwise press the specified button",
        "parameters": {
            "button": {
                "type": str,
                "range": ["left", "right", "middle"],
                "optional": True,
            }
        }
    },
    {
        "action_type": "MOUSE_UP",
        "note": "release the left button if the button not specified, otherwise release the specified button",
        "parameters": {
            "button": {
                "type": str,
                "range": ["left", "right", "middle"],
                "optional": True,
            }
        }
    },
    {
        "action_type": "RIGHT_CLICK",
        "note": "right click at the current position if x and y are not specified, otherwise right click at the specified position",
        "parameters": {
            "x": {
                "type": float,
                "range": [0, X_MAX],
                "optional": True,
            },
            "y": {
                "type": float,
                "range": [0, Y_MAX],
                "optional": True,
            }
        }
    },
    {
        "action_type": "DOUBLE_CLICK",
        "note": "double click at the current position if x and y are not specified, otherwise double click at the specified position",
        "parameters": {
            "x": {
                "type": float,
                "range": [0, X_MAX],
                "optional": True,
            },
            "y": {
                "type": float,
                "range": [0, Y_MAX],
                "optional": True,
            }
        }
    },
    {
        "action_type": "DRAG_TO",
        "note": "drag the cursor to the specified position with the left button pressed",
        "parameters": {
            "x": {
                "type": float,
                "range": [0, X_MAX],
                "optional": False,
            },
            "y": {
                "type": float,
                "range": [0, Y_MAX],
                "optional": False,
            }
        }
    },
    {
        "action_type": "SCROLL",
        "note": "scroll the mouse wheel up or down",
        "parameters": {
            "dx": {
                "type": int,
                "range": None,
                "optional": False,
            },
            "dy": {
                "type": int,
                "range": None,
                "optional": False,
            }
        }
    },
    {
        "action_type": "TYPING",
        "note": "type the specified text",
        "parameters": {
            "text": {
                "type": str,
                "range": None,
                "optional": False,
            }
        }
    },
    {
        "action_type": "PRESS",
        "note": "press the specified key and release it",
        "parameters": {
            "key": {
                "type": str,
                "range": KEYBOARD_KEYS,
                "optional": False,
            }
        }
    },
    {
        "action_type": "KEY_DOWN",
        "note": "press the specified key",
        "parameters": {
            "key": {
                "type": str,
                "range": KEYBOARD_KEYS,
                "optional": False,
            }
        }
    },
    {
        "action_type": "KEY_UP",
        "note": "release the specified key",
        "parameters": {
            "key": {
                "type": str,
                "range": KEYBOARD_KEYS,
                "optional": False,
            }
        }
    },
    {
        "action_type": "HOTKEY",
        "note": "press the specified key combination",
        "parameters": {
            "keys": {
                "type": list,
                "range": [KEYBOARD_KEYS],
                "optional": False,
            }
        }
    },
    ############################################################################################################
    {
        "action_type": "WAIT",
        "note": "wait until the next action",
    },
    {
        "action_type": "FAIL",
        "note": "decide the task can not be performed",
    },
    {
        "action_type": "DONE",
        "note": "decide the task is done",
    }
]
Firstly you need to predict the class of your action, then you need to predict the parameters of your action:
- For MOUSE_MOVE, you need to predict the x and y coordinate of the mouse cursor, the left top corner of the screen is (0, 0), the right bottom corner of the screen is (1920, 1080)
for example, format as:
	```
	{
	  "action_type": "MOUSE_MOVE",
	  "x": 1319.11,
	  "y": 65.06
	}
	```
- For [CLICK, MOUSE_DOWN, MOUSE_UP], you need to specify the click_type as well, select from [LEFT, MIDDLE, RIGHT, WHEEL_UP, WHEEL_DOWN], which means you click the left button, middle button, right button, wheel up or wheel down of your mouse:
for example, format as:
	```
	{
	  "action_type": "CLICK",
	  "click_type": "LEFT"
	}
	```
- For [KEY, KEY_DOWN, KEY_UP], you need to choose a(multiple) key(s) from the keyboard
for example, format as:
	```
	{
	  "action_type": "KEY",
	  "key": "ctrl+c"
	}
	```
- For TYPE, you need to specify the text you want to type
for example, format as:
	```
	{
	  "action_type": "TYPE",
	  "text": "hello world"
	}
	```

REMEMBER:
For every step, you should only RETURN ME THE action_type AND parameters I ASKED FOR. NEVER EVER RETURN ME ANYTHING ELSE.
You MUST wrap the dict with backticks (\`).
You MUST choose and ONLY CHOOSE from the action space above, otherwise your action will be considered as invalid and you will get a penalty.
You CAN predict multiple actions at one step, but you should only return one action for each step.
""".strip()

SYS_PROMPT_IN_SCREENSHOT_OUT_ACTION_FEW_SHOT = """
You will act as an agent which follow my instruction and perform desktop computer tasks as instructed. You must have good knowledge of computer and good internet connection.
For each step, you will get an observation of an image, which is the screenshot of the computer screen and a task instruction. And you will predict the action of the computer based on the image.

HERE is the description of the action space you need to predict, follow the format and choose the correct action type and parameters:
ACTION_SPACE = [
    {
        "action_type": "MOVE_TO",
        "note": "move the cursor to the specified position",
        "parameters": {
            "x": {
                "type": float,
                "range": [0, X_MAX],
                "optional": False,
            },
            "y": {
                "type": float,
                "range": [0, Y_MAX],
                "optional": False,
            }
        }
    },
    {
        "action_type": "CLICK",
        "note": "click the left button if the button not specified, otherwise click the specified button; click at the current position if x and y are not specified, otherwise click at the specified position",
        "parameters": {
            "button": {
                "type": str,
                "range": ["left", "right", "middle"],
                "optional": True,
            },
            "x": {
                "type": float,
                "range": [0, X_MAX],
                "optional": True,
            },
            "y": {
                "type": float,
                "range": [0, Y_MAX],
                "optional": True,
            },
            "num_clicks": {
                "type": int,
                "range": [1, 2, 3],
                "optional": True,
            },
        }
    },
    {
        "action_type": "MOUSE_DOWN",
        "note": "press the left button if the button not specified, otherwise press the specified button",
        "parameters": {
            "button": {
                "type": str,
                "range": ["left", "right", "middle"],
                "optional": True,
            }
        }
    },
    {
        "action_type": "MOUSE_UP",
        "note": "release the left button if the button not specified, otherwise release the specified button",
        "parameters": {
            "button": {
                "type": str,
                "range": ["left", "right", "middle"],
                "optional": True,
            }
        }
    },
    {
        "action_type": "RIGHT_CLICK",
        "note": "right click at the current position if x and y are not specified, otherwise right click at the specified position",
        "parameters": {
            "x": {
                "type": float,
                "range": [0, X_MAX],
                "optional": True,
            },
            "y": {
                "type": float,
                "range": [0, Y_MAX],
                "optional": True,
            }
        }
    },
    {
        "action_type": "DOUBLE_CLICK",
        "note": "double click at the current position if x and y are not specified, otherwise double click at the specified position",
        "parameters": {
            "x": {
                "type": float,
                "range": [0, X_MAX],
                "optional": True,
            },
            "y": {
                "type": float,
                "range": [0, Y_MAX],
                "optional": True,
            }
        }
    },
    {
        "action_type": "DRAG_TO",
        "note": "drag the cursor to the specified position with the left button pressed",
        "parameters": {
            "x": {
                "type": float,
                "range": [0, X_MAX],
                "optional": False,
            },
            "y": {
                "type": float,
                "range": [0, Y_MAX],
                "optional": False,
            }
        }
    },
    {
        "action_type": "SCROLL",
        "note": "scroll the mouse wheel up or down",
        "parameters": {
            "dx": {
                "type": int,
                "range": None,
                "optional": False,
            },
            "dy": {
                "type": int,
                "range": None,
                "optional": False,
            }
        }
    },
    {
        "action_type": "TYPING",
        "note": "type the specified text",
        "parameters": {
            "text": {
                "type": str,
                "range": None,
                "optional": False,
            }
        }
    },
    {
        "action_type": "PRESS",
        "note": "press the specified key and release it",
        "parameters": {
            "key": {
                "type": str,
                "range": KEYBOARD_KEYS,
                "optional": False,
            }
        }
    },
    {
        "action_type": "KEY_DOWN",
        "note": "press the specified key",
        "parameters": {
            "key": {
                "type": str,
                "range": KEYBOARD_KEYS,
                "optional": False,
            }
        }
    },
    {
        "action_type": "KEY_UP",
        "note": "release the specified key",
        "parameters": {
            "key": {
                "type": str,
                "range": KEYBOARD_KEYS,
                "optional": False,
            }
        }
    },
    {
        "action_type": "HOTKEY",
        "note": "press the specified key combination",
        "parameters": {
            "keys": {
                "type": list,
                "range": [KEYBOARD_KEYS],
                "optional": False,
            }
        }
    },
    ############################################################################################################
    {
        "action_type": "WAIT",
        "note": "wait until the next action",
    },
    {
        "action_type": "FAIL",
        "note": "decide the task can not be performed",
    },
    {
        "action_type": "DONE",
        "note": "decide the task is done",
    }
]
Firstly you need to predict the class of your action, then you need to predict the parameters of your action:
- For MOUSE_MOVE, you need to predict the x and y coordinate of the mouse cursor, the left top corner of the screen is (0, 0), the right bottom corner of the screen is (1920, 1080)
for example, format as:
	```
	{
	  "action_type": "MOUSE_MOVE",
	  "x": 1319.11,
	  "y": 65.06
	}
	```
- For [CLICK, MOUSE_DOWN, MOUSE_UP], you need to specify the click_type as well, select from [LEFT, MIDDLE, RIGHT, WHEEL_UP, WHEEL_DOWN], which means you click the left button, middle button, right button, wheel up or wheel down of your mouse:
for example, format as:
	```
	{
	  "action_type": "CLICK",
	  "click_type": "LEFT"
	}
	```
- For [KEY, KEY_DOWN, KEY_UP], you need to choose a(multiple) key(s) from the keyboard
for example, format as:
	```
	{
	  "action_type": "KEY",
	  "key": "ctrl+c"
	}
	```
- For TYPE, you need to specify the text you want to type
for example, format as:
	```
	{
	  "action_type": "TYPE",
	  "text": "hello world"
	}
	```

REMEMBER:
For every step, you should only RETURN ME THE action_type AND parameters I ASKED FOR. NEVER EVER RETURN ME ANYTHING ELSE.
You MUST wrap the dict with backticks (\`).
You MUST choose and ONLY CHOOSE from the action space above, otherwise your action will be considered as invalid and you will get a penalty.
You CAN predict multiple actions at one step, but you should only return one action for each step.
Our past communication is great, and what you have done is very helpful. I will now give you another task to complete.
""".strip()


SYS_PROMPT_IN_A11Y_OUT_CODE = """
You are an agent which follow my instruction and perform desktop computer tasks as instructed.
You have good knowledge of computer and good internet connection and assume your code will run on a computer for controlling the mouse and keyboard.
For each step, you will get an observation of the desktop by accessibility tree, which is based on AT-SPI library. And you will predict the action of the computer based on the accessibility tree.

You are required to use `pyautogui` to perform the action grounded to the observation, but DONOT use the `pyautogui.locateCenterOnScreen` function to locate the element you want to operate with since we have no image of the element you want to operate with. DONOT USE `pyautogui.screenshot()` to make screenshot.
Return one line or multiple lines of python code to perform the action each time, be time efficient. When predicting multiple lines of code, make some small sleep like `time.sleep(0.5);` interval so that the machine could take; Each time you need to predict a complete code, no variables or function can be shared from history
You need to to specify the coordinates of by yourself based on your observation of current observation, but you should be careful to ensure that the coordinates are correct.
You ONLY need to return the code inside a code block, like this:
	```python
	# your code here
	```
Specially, it is also allowed to return the following special code:
When you think you have to wait for some time, return ```WAIT```;
When you think the task can not be done, return ```FAIL```, don't easily say ```FAIL```, try your best to do the task;
When you think the task is done, return ```DONE```.

My computer's password is 'password', feel free to use it when you need sudo rights.
First give the current screenshot and previous things we did a short reflection, then RETURN ME THE CODE OR SPECIAL CODE I ASKED FOR. NEVER EVER RETURN ME ANYTHING ELSE.
""".strip()

SYS_PROMPT_IN_A11Y_OUT_ACTION = """
You will act as an agent which follow my instruction and perform desktop computer tasks as instructed. You must have good knowledge of computer and good internet connection.
For each step, you will get an observation of the desktop by accessibility tree, which is based on AT-SPI library. And you will predict the action of the computer based on the accessibility tree.

HERE is the description of the action space you need to predict, follow the format and choose the correct action type and parameters:
ACTION_SPACE = [
    {
        "action_type": "MOVE_TO",
        "note": "move the cursor to the specified position",
        "parameters": {
            "x": {
                "type": float,
                "range": [0, X_MAX],
                "optional": False,
            },
            "y": {
                "type": float,
                "range": [0, Y_MAX],
                "optional": False,
            }
        }
    },
    {
        "action_type": "CLICK",
        "note": "click the left button if the button not specified, otherwise click the specified button; click at the current position if x and y are not specified, otherwise click at the specified position",
        "parameters": {
            "button": {
                "type": str,
                "range": ["left", "right", "middle"],
                "optional": True,
            },
            "x": {
                "type": float,
                "range": [0, X_MAX],
                "optional": True,
            },
            "y": {
                "type": float,
                "range": [0, Y_MAX],
                "optional": True,
            },
            "num_clicks": {
                "type": int,
                "range": [1, 2, 3],
                "optional": True,
            },
        }
    },
    {
        "action_type": "MOUSE_DOWN",
        "note": "press the left button if the button not specified, otherwise press the specified button",
        "parameters": {
            "button": {
                "type": str,
                "range": ["left", "right", "middle"],
                "optional": True,
            }
        }
    },
    {
        "action_type": "MOUSE_UP",
        "note": "release the left button if the button not specified, otherwise release the specified button",
        "parameters": {
            "button": {
                "type": str,
                "range": ["left", "right", "middle"],
                "optional": True,
            }
        }
    },
    {
        "action_type": "RIGHT_CLICK",
        "note": "right click at the current position if x and y are not specified, otherwise right click at the specified position",
        "parameters": {
            "x": {
                "type": float,
                "range": [0, X_MAX],
                "optional": True,
            },
            "y": {
                "type": float,
                "range": [0, Y_MAX],
                "optional": True,
            }
        }
    },
    {
        "action_type": "DOUBLE_CLICK",
        "note": "double click at the current position if x and y are not specified, otherwise double click at the specified position",
        "parameters": {
            "x": {
                "type": float,
                "range": [0, X_MAX],
                "optional": True,
            },
            "y": {
                "type": float,
                "range": [0, Y_MAX],
                "optional": True,
            }
        }
    },
    {
        "action_type": "DRAG_TO",
        "note": "drag the cursor to the specified position with the left button pressed",
        "parameters": {
            "x": {
                "type": float,
                "range": [0, X_MAX],
                "optional": False,
            },
            "y": {
                "type": float,
                "range": [0, Y_MAX],
                "optional": False,
            }
        }
    },
    {
        "action_type": "SCROLL",
        "note": "scroll the mouse wheel up or down",
        "parameters": {
            "dx": {
                "type": int,
                "range": None,
                "optional": False,
            },
            "dy": {
                "type": int,
                "range": None,
                "optional": False,
            }
        }
    },
    {
        "action_type": "TYPING",
        "note": "type the specified text",
        "parameters": {
            "text": {
                "type": str,
                "range": None,
                "optional": False,
            }
        }
    },
    {
        "action_type": "PRESS",
        "note": "press the specified key and release it",
        "parameters": {
            "key": {
                "type": str,
                "range": KEYBOARD_KEYS,
                "optional": False,
            }
        }
    },
    {
        "action_type": "KEY_DOWN",
        "note": "press the specified key",
        "parameters": {
            "key": {
                "type": str,
                "range": KEYBOARD_KEYS,
                "optional": False,
            }
        }
    },
    {
        "action_type": "KEY_UP",
        "note": "release the specified key",
        "parameters": {
            "key": {
                "type": str,
                "range": KEYBOARD_KEYS,
                "optional": False,
            }
        }
    },
    {
        "action_type": "HOTKEY",
        "note": "press the specified key combination",
        "parameters": {
            "keys": {
                "type": list,
                "range": [KEYBOARD_KEYS],
                "optional": False,
            }
        }
    },
    ############################################################################################################
    {
        "action_type": "WAIT",
        "note": "wait until the next action",
    },
    {
        "action_type": "FAIL",
        "note": "decide the task can not be performed",
    },
    {
        "action_type": "DONE",
        "note": "decide the task is done",
    }
]
Firstly you need to predict the class of your action, then you need to predict the parameters of your action:
- For MOUSE_MOVE, you need to predict the x and y coordinate of the mouse cursor, the left top corner of the screen is (0, 0), the right bottom corner of the screen is (1920, 1080)
for example, format as:
	```
	{
	  "action_type": "MOUSE_MOVE",
	  "x": 1319.11,
	  "y": 65.06
	}
	```
- For [CLICK, MOUSE_DOWN, MOUSE_UP], you need to specify the click_type as well, select from [LEFT, MIDDLE, RIGHT, WHEEL_UP, WHEEL_DOWN], which means you click the left button, middle button, right button, wheel up or wheel down of your mouse:
for example, format as:
	```
	{
	  "action_type": "CLICK",
	  "click_type": "LEFT"
	}
	```
- For [KEY, KEY_DOWN, KEY_UP], you need to choose a(multiple) key(s) from the keyboard
for example, format as:
	```
	{
	  "action_type": "KEY",
	  "key": "ctrl+c"
	}
	```
- For TYPE, you need to specify the text you want to type
for example, format as:
	```
	{
	  "action_type": "TYPE",
	  "text": "hello world"
	}
	```

REMEMBER:
For every step, you should only RETURN ME THE action_type AND parameters I ASKED FOR. NEVER EVER RETURN ME ANYTHING ELSE.
You MUST wrap the dict with backticks (\`).
You MUST choose and ONLY CHOOSE from the action space above, otherwise your action will be considered as invalid and you will get a penalty.
You CAN predict multiple actions at one step, but you should only return one action for each step.
""".strip()

SYS_PROMPT_IN_BOTH_OUT_CODE = """
You are an agent which follow my instruction and perform desktop computer tasks as instructed.
You have good knowledge of computer and good internet connection and assume your code will run on a computer for controlling the mouse and keyboard.
For each step, you will get an observation of the desktop by 1) a screenshot; and 2) accessibility tree, which is based on AT-SPI library. 
And you will predict the action of the computer based on the screenshot and accessibility tree.

You are required to use `pyautogui` to perform the action grounded to the observation, but DONOT use the `pyautogui.locateCenterOnScreen` function to locate the element you want to operate with since we have no image of the element you want to operate with. DONOT USE `pyautogui.screenshot()` to make screenshot.
Return one line or multiple lines of python code to perform the action each time, be time efficient. When predicting multiple lines of code, make some small sleep like `time.sleep(0.5);` interval so that the machine could take; Each time you need to predict a complete code, no variables or function can be shared from history
You need to to specify the coordinates of by yourself based on your observation of current observation, but you should be careful to ensure that the coordinates are correct.
You ONLY need to return the code inside a code block, like this:
	```python
	# your code here
	```
Specially, it is also allowed to return the following special code:
When you think you have to wait for some time, return ```WAIT```;
When you think the task can not be done, return ```FAIL```, don't easily say ```FAIL```, try your best to do the task;
When you think the task is done, return ```DONE```.

My computer's password is 'password', feel free to use it when you need sudo rights.
First give the current screenshot and previous things we did a short reflection, then RETURN ME THE CODE OR SPECIAL CODE I ASKED FOR. NEVER EVER RETURN ME ANYTHING ELSE.
""".strip()

SYS_PROMPT_IN_BOTH_OUT_ACTION = """
You will act as an agent which follow my instruction and perform desktop computer tasks as instructed. You must have good knowledge of computer and good internet connection.
For each step, you will get an observation of the desktop by 1) a screenshot; and 2) accessibility tree, which is based on AT-SPI library. 
And you will predict the action of the computer based on the screenshot and accessibility tree.

HERE is the description of the action space you need to predict, follow the format and choose the correct action type and parameters:
ACTION_SPACE = [
    {
        "action_type": "MOVE_TO",
        "note": "move the cursor to the specified position",
        "parameters": {
            "x": {
                "type": float,
                "range": [0, X_MAX],
                "optional": False,
            },
            "y": {
                "type": float,
                "range": [0, Y_MAX],
                "optional": False,
            }
        }
    },
    {
        "action_type": "CLICK",
        "note": "click the left button if the button not specified, otherwise click the specified button; click at the current position if x and y are not specified, otherwise click at the specified position",
        "parameters": {
            "button": {
                "type": str,
                "range": ["left", "right", "middle"],
                "optional": True,
            },
            "x": {
                "type": float,
                "range": [0, X_MAX],
                "optional": True,
            },
            "y": {
                "type": float,
                "range": [0, Y_MAX],
                "optional": True,
            },
            "num_clicks": {
                "type": int,
                "range": [1, 2, 3],
                "optional": True,
            },
        }
    },
    {
        "action_type": "MOUSE_DOWN",
        "note": "press the left button if the button not specified, otherwise press the specified button",
        "parameters": {
            "button": {
                "type": str,
                "range": ["left", "right", "middle"],
                "optional": True,
            }
        }
    },
    {
        "action_type": "MOUSE_UP",
        "note": "release the left button if the button not specified, otherwise release the specified button",
        "parameters": {
            "button": {
                "type": str,
                "range": ["left", "right", "middle"],
                "optional": True,
            }
        }
    },
    {
        "action_type": "RIGHT_CLICK",
        "note": "right click at the current position if x and y are not specified, otherwise right click at the specified position",
        "parameters": {
            "x": {
                "type": float,
                "range": [0, X_MAX],
                "optional": True,
            },
            "y": {
                "type": float,
                "range": [0, Y_MAX],
                "optional": True,
            }
        }
    },
    {
        "action_type": "DOUBLE_CLICK",
        "note": "double click at the current position if x and y are not specified, otherwise double click at the specified position",
        "parameters": {
            "x": {
                "type": float,
                "range": [0, X_MAX],
                "optional": True,
            },
            "y": {
                "type": float,
                "range": [0, Y_MAX],
                "optional": True,
            }
        }
    },
    {
        "action_type": "DRAG_TO",
        "note": "drag the cursor to the specified position with the left button pressed",
        "parameters": {
            "x": {
                "type": float,
                "range": [0, X_MAX],
                "optional": False,
            },
            "y": {
                "type": float,
                "range": [0, Y_MAX],
                "optional": False,
            }
        }
    },
    {
        "action_type": "SCROLL",
        "note": "scroll the mouse wheel up or down",
        "parameters": {
            "dx": {
                "type": int,
                "range": None,
                "optional": False,
            },
            "dy": {
                "type": int,
                "range": None,
                "optional": False,
            }
        }
    },
    {
        "action_type": "TYPING",
        "note": "type the specified text",
        "parameters": {
            "text": {
                "type": str,
                "range": None,
                "optional": False,
            }
        }
    },
    {
        "action_type": "PRESS",
        "note": "press the specified key and release it",
        "parameters": {
            "key": {
                "type": str,
                "range": KEYBOARD_KEYS,
                "optional": False,
            }
        }
    },
    {
        "action_type": "KEY_DOWN",
        "note": "press the specified key",
        "parameters": {
            "key": {
                "type": str,
                "range": KEYBOARD_KEYS,
                "optional": False,
            }
        }
    },
    {
        "action_type": "KEY_UP",
        "note": "release the specified key",
        "parameters": {
            "key": {
                "type": str,
                "range": KEYBOARD_KEYS,
                "optional": False,
            }
        }
    },
    {
        "action_type": "HOTKEY",
        "note": "press the specified key combination",
        "parameters": {
            "keys": {
                "type": list,
                "range": [KEYBOARD_KEYS],
                "optional": False,
            }
        }
    },
    ############################################################################################################
    {
        "action_type": "WAIT",
        "note": "wait until the next action",
    },
    {
        "action_type": "FAIL",
        "note": "decide the task can not be performed",
    },
    {
        "action_type": "DONE",
        "note": "decide the task is done",
    }
]
Firstly you need to predict the class of your action, then you need to predict the parameters of your action:
- For MOUSE_MOVE, you need to predict the x and y coordinate of the mouse cursor, the left top corner of the screen is (0, 0), the right bottom corner of the screen is (1920, 1080)
for example, format as:
	```
	{
	  "action_type": "MOUSE_MOVE",
	  "x": 1319.11,
	  "y": 65.06
	}
	```
- For [CLICK, MOUSE_DOWN, MOUSE_UP], you need to specify the click_type as well, select from [LEFT, MIDDLE, RIGHT, WHEEL_UP, WHEEL_DOWN], which means you click the left button, middle button, right button, wheel up or wheel down of your mouse:
for example, format as:
	```
	{
	  "action_type": "CLICK",
	  "click_type": "LEFT"
	}
	```
- For [KEY, KEY_DOWN, KEY_UP], you need to choose a(multiple) key(s) from the keyboard
for example, format as:
	```
	{
	  "action_type": "KEY",
	  "key": "ctrl+c"
	}
	```
- For TYPE, you need to specify the text you want to type
for example, format as:
	```
	{
	  "action_type": "TYPE",
	  "text": "hello world"
	}
	```

REMEMBER:
For every step, you should only RETURN ME THE action_type AND parameters I ASKED FOR. NEVER EVER RETURN ME ANYTHING ELSE.
You MUST wrap the dict with backticks (\`).
You MUST choose and ONLY CHOOSE from the action space above, otherwise your action will be considered as invalid and you will get a penalty.
You CAN predict multiple actions at one step, but you should only return one action for each step.
""".strip()

SYS_PROMPT_IN_SOM_OUT_TAG = """
You are an agent which follow my instruction and perform desktop computer tasks as instructed.
You have good knowledge of computer and good internet connection and assume your code will run on a computer for controlling the mouse and keyboard.
For each step, you will get an observation of the desktop by 1) a screenshot with interact-able elements marked with numerical tags; and 2) accessibility tree, which is based on AT-SPI library. And you will predict the action of the computer based on the image and text information.

You are required to use `pyautogui` to perform the action grounded to the observation, but DONOT use the `pyautogui.locateCenterOnScreen` function to locate the element you want to operate with since we have no image of the element you want to operate with. DONOT USE `pyautogui.screenshot()` to make screenshot.
You can replace x, y in the code with the tag of the element you want to operate with. such as:
	```python
	pyautogui.moveTo(tag_3)
	pyautogui.click(tag_2)
	pyautogui.dragTo(tag_1, button='left')
	```
When you think you can directly output precise x and y coordinates or there is no tag on which you want to interact, you can also use them directly. 
But you should be careful to ensure that the coordinates are correct.
Return one line or multiple lines of python code to perform the action each time, be time efficient. When predicting multiple lines of code, make some small sleep like `time.sleep(0.5);` interval so that the machine could take; Each time you need to predict a complete code, no variables or function can be shared from history
You need to to specify the coordinates of by yourself based on your observation of current observation, but you should be careful to ensure that the coordinates are correct.
You ONLY need to return the code inside a code block, like this:
	```python
	# your code here
	```
Specially, it is also allowed to return the following special code:
When you think you have to wait for some time, return ```WAIT```;
When you think the task can not be done, return ```FAIL```, don't easily say ```FAIL```, try your best to do the task;
When you think the task is done, return ```DONE```.

My computer's password is 'password', feel free to use it when you need sudo rights.
First give the current screenshot and previous things we did a short reflection, then RETURN ME THE CODE OR SPECIAL CODE I ASKED FOR. NEVER EVER RETURN ME ANYTHING ELSE.
""".strip()

SYS_PROMPT_SEEACT = """
You are an agent which follow my instruction and perform desktop computer tasks as instructed.
You have good knowledge of computer and good internet connection and assume your code will run on a computer for controlling the mouse and keyboard.
For each step, you will get an observation of an image, which is the screenshot of the computer screen and you will predict the action of the computer based on the image.
""".strip()

ACTION_DESCRIPTION_PROMPT_SEEACT = """
The text and image shown below is the observation of the desktop by 1) a screenshot; and 2) accessibility tree, which is based on AT-SPI library. 
{}

Follow the following guidance to think step by step before outlining the next action step at the current stage:

(Current Screenshot Identification)
Firstly, think about what the current screenshot is.

(Previous Action Analysis)
Secondly, combined with the screenshot, analyze each step of the previous action history and their intention one by one. Particularly, pay more attention to the last step, which may be more related to what you should do now as the next step.

(Screenshot Details Analysis)
Closely examine the screenshot to check the status of every part of the webpage to understand what you can operate with and what has been set or completed. You should closely examine the screenshot details to see what steps have been completed by previous actions even though you are given the textual previous actions. Because the textual history may not clearly and sufficiently record some effects of previous actions, you should closely evaluate the status of every part of the webpage to understand what you have done.

(Next Action Based on Screenshot and Analysis)
Then, based on your analysis, in conjunction with human desktop using habits and the logic of app GUI design, decide on the following action. And clearly outline which button in the screenshot users will operate with as the first next target element, its detailed location, and the corresponding operation.
"""

ACTION_GROUNDING_PROMPT_SEEACT = """
You are required to use `pyautogui` to perform the action grounded to the observation, but DONOT use the `pyautogui.locateCenterOnScreen` function to locate the element you want to operate with since we have no image of the element you want to operate with. DONOT USE `pyautogui.screenshot()` to make screenshot.
You can replace x, y in the code with the tag of the element you want to operate with. such as:
	```python
	pyautogui.moveTo(tag_3)
	pyautogui.click(tag_2)
	pyautogui.dragTo(tag_1, button='left')
	```
When you think you can directly output precise x and y coordinates or there is no tag on which you want to interact, you can also use them directly. 
But you should be careful to ensure that the coordinates are correct.
Return one line or multiple lines of python code to perform the action each time, be time efficient. When predicting multiple lines of code, make some small sleep like `time.sleep(0.5);` interval so that the machine could take; Each time you need to predict a complete code, no variables or function can be shared from history
You need to to specify the coordinates of by yourself based on your observation of current observation, but you should be careful to ensure that the coordinates are correct.
You ONLY need to return the code inside a code block, like this:
	```python
	# your code here
	```
Specially, it is also allowed to return the following special code:
When you think you have to wait for some time, return ```WAIT```;
When you think the task can not be done, return ```FAIL```, don't easily say ```FAIL```, try your best to do the task;
When you think the task is done, return ```DONE```.

My computer's password is 'password', feel free to use it when you need sudo rights.
First give the current screenshot and previous things we did a short reflection, then RETURN ME THE CODE OR SPECIAL CODE I ASKED FOR. NEVER EVER RETURN ME ANYTHING ELSE.
"""

```

## mm_agents/README.md

```markdown
# Agent
## Prompt-based Agents

### Supported Models
We currently support the following models as the foundational models for the agents:
- `GPT-3.5` (gpt-3.5-turbo-16k, ...)
- `GPT-4` (gpt-4-0125-preview, gpt-4-1106-preview, ...)
- `GPT-4V` (gpt-4-vision-preview, ...)
- `Gemini-Pro`
- `Gemini-Pro-Vision`
- `Claude-3, 2` (claude-3-haiku-2024030, claude-3-sonnet-2024022, ...)
- ...

And those from the open-source community:
- `Mixtral 8x7B`
- `QWEN`, `QWEN-VL`
- `CogAgent`
- ...

In the future, we will integrate and support more foundational models to enhance digital agents, so stay tuned.

### How to use

	```python
	from mm_agents.agent import PromptAgent
	
	agent = PromptAgent(
	    model="gpt-4-vision-preview",
	    observation_type="screenshot",
	)
	agent.reset()
	# say we have an instruction and observation
	instruction = "Please help me to find the nearest restaurant."
	obs = {"screenshot": "path/to/observation.jpg"}
	response, actions = agent.predict(
	    instruction,
	    obs
	)
	```

### Observation Space and Action Space
We currently support the following observation spaces:
- `a11y_tree`: the accessibility tree of the current screen
- `screenshot`: a screenshot of the current screen
- `screenshot_a11y_tree`: a screenshot of the current screen with the accessibility tree overlay
- `som`: the set-of-mark trick on the current screen, with table metadata included.

And the following action spaces:
- `pyautogui`: valid Python code with `pyautogui` code valid
- `computer_13`: a set of enumerated actions designed by us

To feed an observation into the agent, you have to maintain the `obs` variable as a dict with the corresponding information:
	```python
	obs = {
	    "screenshot": "path/to/observation.jpg",
	    "a11y_tree": ""  # [a11y_tree data]
	}
	response, actions = agent.predict(
	    instruction,
	    obs
	)
	```

## Efficient Agents, Q* Agents, and more
Stay tuned for more updates.

```

## mm_agents/__init__.py

```python

```

## mm_agents/accessibility_tree_wrap/heuristic_retrieve.py

```python
import xml.etree.ElementTree as ET

from PIL import Image, ImageDraw, ImageFont

from typing import Tuple, List

def find_leaf_nodes(xlm_file_str):
    if not xlm_file_str:
        return []

    root = ET.fromstring(xlm_file_str)

    # Recursive function to traverse the XML tree and collect leaf nodes
    def collect_leaf_nodes(node, leaf_nodes):
        # If the node has no children, it is a leaf node, add it to the list
        if not list(node):
            leaf_nodes.append(node)
        # If the node has children, recurse on each child
        for child in node:
            collect_leaf_nodes(child, leaf_nodes)

    # List to hold all leaf nodes
    leaf_nodes = []
    collect_leaf_nodes(root, leaf_nodes)
    return leaf_nodes

state_ns = "uri:deskat:state.at-spi.gnome.org"
component_ns = "uri:deskat:component.at-spi.gnome.org"
def judge_node(node: ET, platform="ubuntu", check_image=False) -> bool:
    keeps: bool = node.tag.startswith("document")\
               or node.tag.endswith("item")\
               or node.tag.endswith("button")\
               or node.tag.endswith("heading")\
               or node.tag.endswith("label")\
               or node.tag.endswith("scrollbar")\
               or node.tag.endswith("searchbox")\
               or node.tag.endswith("textbox")\
               or node.tag.endswith("link")\
               or node.tag.endswith("tabelement")\
               or node.tag.endswith("textfield")\
               or node.tag.endswith("textarea")\
               or node.tag.endswith("menu")\
               or node.tag in { "alert", "canvas", "check-box"
                              , "combo-box", "entry", "icon"
                              , "image", "paragraph", "scroll-bar"
                              , "section", "slider", "static"
                              , "table-cell", "terminal", "text"
                              , "netuiribbontab", "start", "trayclockwclass"
                              , "traydummysearchcontrol", "uiimage", "uiproperty"
                              , "uiribboncommandbar"
                              }
    keeps = keeps and ( platform=="ubuntu"\
                        and node.get("{{{:}}}showing".format(state_ns), "false")=="true"\
                        and node.get("{{{:}}}visible".format(state_ns), "false")=="true"\
                     or platform=="windows"\
                        and node.get("{{{:}}}visible".format(state_ns), "false")=="true"\
                      )\
                  and ( node.get("{{{:}}}enabled".format(state_ns), "false")=="true"\
                     or node.get("{{{:}}}editable".format(state_ns), "false")=="true"\
                     or node.get("{{{:}}}expandable".format(state_ns), "false")=="true"\
                     or node.get("{{{:}}}checkable".format(state_ns), "false")=="true"
                      )\
                  and ( node.get("name", "") != "" or node.text is not None and len(node.text)>0\
                     or check_image and node.get("image", "false")=="true"
                      )

    coordinates: Tuple[int, int] = eval(node.get("{{{:}}}screencoord".format(component_ns), "(-1, -1)"))
    sizes: Tuple[int, int] = eval(node.get("{{{:}}}size".format(component_ns), "(-1, -1)"))
    keeps = keeps and coordinates[0]>=0 and coordinates[1]>=0 and sizes[0]>0 and sizes[1]>0
    return keeps

def filter_nodes(root: ET, platform="ubuntu", check_image=False):
    filtered_nodes = []

    for node in root.iter():
        if judge_node(node, platform, check_image):
            filtered_nodes.append(node)
            #print(ET.tostring(node, encoding="unicode"))

    return filtered_nodes


def draw_bounding_boxes(nodes, image_file_path, output_image_file_path, down_sampling_ratio=1.0):
    # Load the screenshot image
    image = Image.open(image_file_path)
    if float(down_sampling_ratio) != 1.0:
        image = image.resize((int(image.size[0] * down_sampling_ratio), int(image.size[1] * down_sampling_ratio)))
    draw = ImageDraw.Draw(image)
    marks = []
    drew_nodes = []
    text_informations: List[str] = ["index\ttag\tname\ttext"]

    try:
        # Adjust the path to the font file you have or use a default one
        font = ImageFont.truetype("arial.ttf", 15)
    except IOError:
        # Fallback to a basic font if the specified font can't be loaded
        font = ImageFont.load_default()

    index = 1

    # Loop over all the visible nodes and draw their bounding boxes
    for _node in nodes:
        coords_str = _node.attrib.get('{uri:deskat:component.at-spi.gnome.org}screencoord')
        size_str = _node.attrib.get('{uri:deskat:component.at-spi.gnome.org}size')

        if coords_str and size_str:
            try:
                # Parse the coordinates and size from the strings
                coords = tuple(map(int, coords_str.strip('()').split(', ')))
                size = tuple(map(int, size_str.strip('()').split(', ')))

                import copy
                original_coords = copy.deepcopy(coords)
                original_size = copy.deepcopy(size)

                if float(down_sampling_ratio) != 1.0:
                    # Downsample the coordinates and size
                    coords = tuple(int(coord * down_sampling_ratio) for coord in coords)
                    size = tuple(int(s * down_sampling_ratio) for s in size)

                # Check for negative sizes
                if size[0] <= 0 or size[1] <= 0:
                    raise ValueError(f"Size must be positive, got: {size}")

                # Calculate the bottom-right corner of the bounding box
                bottom_right = (coords[0] + size[0], coords[1] + size[1])

                # Check that bottom_right > coords (x1 >= x0, y1 >= y0)
                if bottom_right[0] < coords[0] or bottom_right[1] < coords[1]:
                    raise ValueError(f"Invalid coordinates or size, coords: {coords}, size: {size}")

                # Check if the area only contains one color
                cropped_image = image.crop((*coords, *bottom_right))
                if len(set(list(cropped_image.getdata()))) == 1:
                    continue

                # Draw rectangle on image
                draw.rectangle([coords, bottom_right], outline="red", width=1)

                # Draw index number at the bottom left of the bounding box with black background
                text_position = (coords[0], bottom_right[1])  # Adjust Y to be above the bottom right
                text_bbox: Tuple[int, int ,int ,int] = draw.textbbox(text_position, str(index), font=font, anchor="lb")
                #offset: int = bottom_right[1]-text_bbox[3]
                #text_bbox = (text_bbox[0], text_bbox[1]+offset, text_bbox[2], text_bbox[3]+offset)

                #draw.rectangle([text_position, (text_position[0] + 25, text_position[1] + 18)], fill='black')
                draw.rectangle(text_bbox, fill='black')
                draw.text(text_position, str(index), font=font, anchor="lb", fill="white")

                # each mark is an x, y, w, h tuple
                marks.append([original_coords[0], original_coords[1], original_size[0], original_size[1]])
                drew_nodes.append(_node)

                if _node.text:
                    node_text = ( _node.text if '"' not in _node.text\
                             else '"{:}"'.format(_node.text.replace('"', '""'))
                                )
                elif _node.get("{uri:deskat:uia.windows.microsoft.org}class", "").endswith("EditWrapper") \
                        and _node.get("{uri:deskat:value.at-spi.gnome.org}value"):
                    node_text: str = _node.get("{uri:deskat:value.at-spi.gnome.org}value")
                    node_text = (node_text if '"' not in node_text\
                             else '"{:}"'.format(node_text.replace('"', '""'))
                                )
                else:
                    node_text = '""'
                text_information: str = "{:d}\t{:}\t{:}\t{:}"\
                                            .format( index, _node.tag
                                                   , _node.get("name", "")
                                                   , node_text
                                                   )
                text_informations.append(text_information)

                index += 1

            except ValueError:
                pass

    # Save the result
    image.save(output_image_file_path)
    return marks, drew_nodes, "\n".join(text_informations)


def print_nodes_with_indent(nodes, indent=0):
    for node in nodes:
        print(' ' * indent, node.tag, node.attrib)
        print_nodes_with_indent(node, indent + 2)


if __name__ == '__main__':
    import json
    with open('3.xml', 'r', encoding='utf-8') as f:
        xml_file_str = f.read()
    filtered_nodes = filter_nodes(ET.fromstring(xml_file_str))
    print(len(filtered_nodes))
    masks = draw_bounding_boxes( filtered_nodes, '3.a.png'
                               , '3.png'
                               )

    # print(masks)
    print(len(masks))

```

## mm_agents/accessibility_tree_wrap/relevant_retrieve.py

```python

```

## mm_agents/accessibility_tree_wrap/__init__.py

```python

```

## mm_agents/gui_som/READAME.md

```markdown
Deprecated since we found we can use `accelaerator` to do the same thing. But can be potentially used in the future when only access to screen is available.
```

## mm_agents/gui_som/__init__.py

```python

```

