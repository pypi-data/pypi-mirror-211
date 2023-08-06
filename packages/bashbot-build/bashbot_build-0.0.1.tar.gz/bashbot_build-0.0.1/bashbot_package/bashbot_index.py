import os
import sys
import openai
import requests
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt

# CURRENT FLAGS:
# -S [save_lang] (save code or no)
# -P [save_path] (specify path to save code)
# -L (enable logging)
# -N [save_name] (specify code output save name)

# to do:

# detect shortage of openAI tokens
# error handling in general


# openAI Key (REMOVE LATER!!): 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


console = Console()

# Global config variables =======================================
debug = True
usage = "[red bold]Usage: bash-bot \[script_flag = -S] \[script_lang = py/js/jsx/c]"
save_code = False
save_path = os.path.abspath('')
save_name = "bashbot_code"
logging = False
code_lang = ""
system_msg = "You are an AI bot built especially to help programmers."
# msgs = [{"role": "system", "content": system_msg}]
avail_langs = ['py', 'js', 'jsx', 'c']
lang_config = {
    "py": {
        "name": "python",
        'code_run': 'python ',
        'ext': '.py',
        'comment': '# '
    },
    'js': {
        'name': 'javascript',
        'code_run': 'node ',
        'ext': '.js',
        'comment': '// '
    },
    'jsx': {
        'name': 'JSX',
        'code_run': 'echo This file cannot be run by itself ~ ',
        'ext': '.js',
        'comment': '// '
    },
    'c': {
        'name': 'C',
        'code_run': 'clang ',
        'post_run': './a.out',
        'ext': '.c',
        'comment': '// '
    }
}
# ==============================================================



def safe_find(lst, item):
    for i in range(len(lst)):
        if item == lst[i]:
            return i
    return -1


# New flexible argument handler
def parse_arguments():
    global save_code, save_name, save_path, logging, code_lang, debug, system_msg, lang_config

    # if autosave flag is on
    if safe_find(sys.argv, '-S') > 0:
        save_flag_index = safe_find(sys.argv, '-S')
        try: 
            if avail_langs.count(sys.argv[save_flag_index + 1]) > 0:
                save_code = True
                code_lang = sys.argv[save_flag_index + 1]
                if save_code:
                    system_msg = system_msg + " Whenever asked to generate code, you will do so only in {}. If asked to generate code in other languages, you should warn the user.".format(lang_config[code_lang]['name'])
                path_flag_index = safe_find(sys.argv, '-P')
                save_name_index = safe_find(sys.argv, '-N')
                if path_flag_index > 0:
                    save_path = os.path.abspath(sys.argv[path_flag_index + 1])
                if save_name_index > 0:
                    # Sanitize or reject dangerous names
                    save_name = sys.argv[save_name_index + 1]
                    if os.path.isfile(save_path + '/' + save_name + lang_config[code_lang]['ext']):
                        console.print('[bold red]A file by this name already exists at this location. Please choose a different name or delete the existing file.')
                        exit()
                console.print("[green]Autosave enabled. Code will be saved at " + save_path + '/' + save_name + lang_config[code_lang]['ext'])
            else:
                console.print(usage)
                exit()
        except Exception as err:
            print('Error while parsing arguments: ', err)
            console.print('[red]Use `bashbot -H` to see the available arguments')
            exit()
    
    # if logging flag is on
    if safe_find(sys.argv, '-L') > 0:
        logfile = open(save_path + '/bashbot.log', 'w')
        logfile.write('Bashbot Logs: \n')
        logfile.close()
        console.print('[yellow]Logging enabled. Logs can be found at ' + save_path + '/bashbot.log')
        logging = True
    
    # debugging information
    if debug:
        print('save_code: ', save_code)
        print('save_name: ', save_name)
        print('save_path: ', save_path)
        print('logging: ', logging)
        print('code_lang: ', code_lang)
        print('system_msg: ', system_msg)

# log_code(txt) writes BashBot interactions to a .log file at specified location
def log_code(txt):
    logfile = open(save_path + '/bashbot.log', 'a')
    logfile.write('==================================================== \n')
    logfile.write(txt + '\n')
    logfile.close()

# runProg() runs the code stored as per filename and path specified by global config vars
def runProg():
    if save_code:
        console.print("[green bold]Your program in " + lang_config[code_lang]['name'] + " is being executed")
        os.system(lang_config[code_lang]['code_run'] + save_name + lang_config[code_lang]['ext'])
        if code_lang == 'c':
            os.system(lang_config[code_lang]['post_run'])
        console.print("[green bold]Your program in " + lang_config[code_lang]['name'] + " has been executed")
        


# bot_funcs(user_inp) checks for and (if applicable) executes special commands that do not interact with openAI
# -1 means terminate, 0 means skip to next iteration, 1 means continue with current iteration
def bot_funcs(user_inp):
    if user_inp == 'exit':
            console.print("[red bold]Session terminated")
            return -1
    elif user_inp == 'run':
        if save_code:
            runProg()
            return 0
        else:
            console.print("[red bold]To autosave generated code, use the -s flag when starting BashBot")
            return 0
    elif user_inp == 'open':
        if save_code:
            os.system('vim ' + save_path + '/' + save_name + lang_config[code_lang]['ext'])
            return 0
        else:
            console.print("[red bold]To autosave generated code, use the -S flag when starting BashBot")
            return 0
    elif user_inp == 'console':
        console.print('[bold blue]In Console mode, enter "exit_console" to go back to BashBot')
        console.print('[bold red]Note: commands that change directories may not function as expected')
        while True:
            cmd = Prompt.ask('[bold green]Console')
            if cmd == 'exit_console':
                break
            os.system(cmd)
        return 0
    elif user_inp == 'clear':
        os.system('clear')
        return 0
    else:
        return 1

# write_code(bot_res) extracts and writes the first code block in bot_res to filename and path specified by global config vars
def write_code(bot_res):
    code_block_start = bot_res.find("```")
    if code_block_start != -1:
        code_block_end = bot_res.find("```", code_block_start + 1)
        code = bot_res[code_block_start:code_block_end]
        codefile = open(save_path + '/' + save_name + lang_config[code_lang]['ext'], "w")
        codefile.write(lang_config[code_lang]['comment'] + code)
        codefile.close()
        return True

# config() handles the input and storage of credentials
# may create a file at the root directory
def config():
    
    openai_key = Prompt.ask('openAI API Key')
    license_key = Prompt.ask('Purchased license key')

    # Returns info about key if it exists
    key_info = requests.post('https://api.lemonsqueezy.com/v1/licenses/validate',
    {
        'license_key': license_key
    }).json()
    
    # if key is not valid, then exit
    if not key_info['valid']:
        console.print('[red]The provided license key is not valid')
        exit()

    # if activation limit reached, then exit
    if key_info['license_key']['activation_usage'] == key_info['license_key']['activation_limit']:
        console.print('[red]This license key is already in use. Please enter a new key.')
        exit()

    # if we haven't exited by now, the key is valid and can be activated, hence activate
    activation = requests.post('https://api.lemonsqueezy.com/v1/licenses/activate',
        {
            'license_key': license_key,
            'instance_name': 'user_' + license_key
        }).json()
  
    # if valid:
    configfile = open(os.path.expanduser('~/bashbot_config.txt'), "w")
    configfile.write(openai_key + '\n')
    configfile.write(license_key + '\n')
    configfile.write(activation['instance']['id'] + '\n')
    console.print('[green]BashBot configuration completed successfully.')
    configfile.close()

    # if not valid:
    # console.print('[red]One or both of the provided keys are invalid. Please try again with valid keys.')
    
# is_instance_valid(license_key, instance_id) checks if the LemonSqueezy License Key and Instance ID is valid
def is_instance_valid(license_key, instance_id):
    key_info = requests.post('https://api.lemonsqueezy.com/v1/licenses/validate',
    {
        'license_key': license_key,
        'instance_id': instance_id
    }).json()
    return key_info['valid']

# Main entry point for the CLI tool
def start():

    # handling `bashbot config`
    if len(sys.argv) == 2 and sys.argv[1] == 'config':
        config()
        exit()
    
    # Checking for existence of config file at user home directory 
    if not os.path.isfile(os.path.expanduser('~/bashbot_config.txt')):
        console.print('[bold red]BashBot not configured correctly. Run `bashbot-cli config \[openAI API Key]` to configure BashBot')
        exit()
    
    # reading credentials
    configfile = open(os.path.expanduser('~/bashbot_config.txt'), "r")
    configlines = list(configfile)
    if not len(configlines) == 3:
        console.print('[bold red]BashBot not configured correctly. Run `bashbot config` to configure BashBot before use.')
        exit()
    openai.api_key = configlines[0][:-1]
    ls_license_key = configlines[1][:-1]
    ls_instance_id = configlines[2][:-1]

    configfile.close()

    # checking credentials
    if not is_instance_valid(ls_license_key, ls_instance_id):
        console.print('[red]Invalid license key being used. Run `bashbot config` to activate a new key')
        exit()


    parse_arguments()
    msgs = [{"role": "system", "content": system_msg}]

    console.print('[blue]Started new BashBot session')

    # each question/answer iteration
    while True:
        inp = Prompt.ask("[magenta][b]You")
        state = bot_funcs(inp)
        if state == -1:
            exit()
        elif state == 0:
            continue

        msgs.append({"role": "user", "content": inp})

        try: 
            response = openai.ChatCompletion.create(
                model = 'gpt-3.5-turbo',
                messages = msgs
            )
            response_txt = response.choices[0].message.content
            code_saved = False
            if save_code:
                code_saved = write_code(response_txt)
            if logging:
                log_code('You: ' + inp + '\nBashBot: ' + response_txt)

            console.print("[blue][b]BashBot: [/blue][/b]")
            console.print(Markdown(response_txt))
            
            if code_saved:
                console.print("[blue bold]Generated code has been saved. Enter 'run' to execute and 'open' to open it in vim.")

            if response.choices[0].finish_reason == 'stop':
                msgs.append(response.choices[0].message)
        except openai.error.AuthenticationError as err:
            console.print('[red]Failed to connect to OpenAI. Make sure your OpenAI API key is valid. Run `bashbot config` to reset keys.')
            exit()
        
        


# start()
# console.print(os.path.expanduser('~/bashbot_config.txt'))