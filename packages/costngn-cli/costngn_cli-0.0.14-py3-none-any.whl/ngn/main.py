from zlib import Z_NO_COMPRESSION
import pkg_resources  # part of setuptools
import typer
from ngn.config.config import *
#from ngn.config.classes import *
from ngn.aws.data import *
from ngn.do.data import *
from ngn.het.data import *
from ngn.lin.data import *
import pandas as pd
import csv
from termcolor import colored
from tabulate import tabulate
#from matplotlib import pyplot as plt
#from matplotlib.widgets import Slider
#from IPython.display import display
#from setup import version

app = typer.Typer(help='* costngn-cli gives you access to cloud services data and costs')


def choose_acc(company):
    print("Reading configuration file") #config.toml        
    #config_file=os.path.join(Path.home(), 'costngn','config.toml')    
    prof=toml.load(config_file)
    #Choose the first account found for this provider    
    have_acc=False
    for pro_nick in prof:
        #pp.pprint(prof[pro_nick]['provider'])
        if prof[pro_nick]['provider'].lower()==company:
            have_acc=True
            nick=pro_nick #acc=prof[nick] #pp.pprint(acc)                       
            print(company.upper(),'account found with nickname',nick)
            break
    if not have_acc:
        print(company.upper(),'account not found in profile')
        quit()
    return nick


def rep_table(nick, rep, company): 
    
    pd.set_option('display.max_rows', None); pd.set_option('display.max_columns', None)
    pd.set_option('display.width', os.get_terminal_size().columns)
    #pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.colheader_justify', 'right') 
    pd.set_option('index',False)
    
    columns=[] 
    rows=[]
 
    for out in inst_out_list:
        rows.append(colored(lab_dict[out],'green'))         

    #for i,inst in enumerate(rep['instances']):
    #    columns.append(colored('Inst '+str(i+1),'yellow'))

    df = pd.DataFrame(index=rows)
    #df= pd.DataFrame(index=rows)    
    for i,inst in enumerate(rep['instances']):
        ## translate company complete name for readability
        inst['prov_full']=comp_dict[inst['provider'].lower()]


        ### CALCULATE COSTS
        #hours elapsed since creation date
        #print(inst['birthday'])
        birth_obj = datetime.strptime(inst['birthday'], birth_format)
        period= (datetime.now()-birth_obj).total_seconds()//3600
        inst['life_cost']= round(period *float(inst['ihprice']),2)
        #hours elapsed on current month
        #period_start=date.today().replace(day=1)
        month_first_day=date.today().replace(day=1)
        zero_hour=datetime.min.time()
        period_start= datetime.combine(month_first_day,zero_hour)
        #print(period_start)        
        if period_start<=birth_obj:period_start=birth_obj
        #period_end=date.today()
        period= (datetime.now()-period_start).total_seconds()//3600      
        #period = (period_end - period_start).days * 24 + datetime.now().hour 

        inst['month_cost']= round(period *float(inst['ihprice']),2)  
        rep['month_cost']+= inst['month_cost']
        rep['life_cost']+= inst['life_cost']
        ### END CALCULATE COSTS

        col_out=[]
        for inst_out in inst_out_list:
            #col_out.append(colored(inst[inst_out],'white'))
            col_out.append(inst[inst_out])
        #col_head=colored('Instance '+str(i+1)+'','green')
        col_head='Instance '+str(i+1)+'         '
        
        df[col_head]=col_out
        #df[colored('Instance '+str(i+1)+'','green')]=col_out
        #df['Instance '+str(i+1)+'         ']=col_out
        #df[i+1]=col_out    
     
    rep['month_cost']= round(rep['month_cost'],2)
    rep['life_cost']= round(rep['life_cost'],2)

    #df = pd.DataFrame(table, columns = columns, index=rows)
    #df = colored(df,'green')
    #result = df.to_string(header = False) #does not work with max width
    #result =df.to_markdown() #does not work with max width
    print('')  
      
    #df.columns(Index=False)

    
    pp.pprint(df)
    #print(tabulate(df, showindex=True, headers=df.columns))
    #print(df.to_string(index=False))
    #print(df.to_string()) #does not paginate
    #df.style #it is not for terminal
    
    ## TABLE FOOTER
    print('')
    print(colored('Total Instances: ','green'),len(rep['instances']))
    print(colored('Current Month Total Estimated Accumulated Cost: ','green'),rep['month_cost'])
    print(colored('Life Total Estimated Accumulated Cost: ','green'),rep['life_cost'])
    
    print('')   


    ### Generate output file
    #if os.path.exists(result_path): print(f'Folder {result_path} already exists')
    #else:
    if not os.path.exists(result_path):     
        print('Making new folder',result_path)
        os.makedirs(result_path)

    base_name=company.lower()+'_'+nick.lower()+ date.today().strftime("_%Y%m%d_")\
        +datetime.now().strftime("%H%M%S") 

    ## JSON file
    report_file=os.path.join(result_path,base_name)+'.json'
    rep_json = json.dumps(rep,indent=2)
    with open(report_file, 'w') as outfile:
        outfile.write(rep_json)
        print('Reports saved to:') 
        print(report_file)
    ## CSV file
    report_file=os.path.join(result_path,base_name)+'.csv'    
    with open(report_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=rep['instances'][0].keys())   
        writer.writeheader()
        writer.writerows(rep['instances'])
        writer.writerow({'id':len(rep['instances']),'name':'<-- Total Instances',
            'avzone':'Total Estimated Accumulated Costs --> ',
            'month_cost':rep['month_cost'],'life_cost':rep['life_cost']})
       

    print(report_file)

def nick_ok(company,nick):
    print("Reading configuration file") #config.toml
    prof=toml.load(config_file)
    #Check if an account with that nickname exists and match the company    
    if nick in prof:
        print(f"Nickname {nick}",end=' ')
        if prof[nick]['provider']==company:
            print(f'matches an account on {comp_dict[company]}')
            return
        else:
            print('does not match any account in',comp_dict[company],', it points to an account in', comp_dict[prof[nick]['provider']])
            quit()
    else:
        print(f"There isn't any account with nickname {nick} in config file\n")
        print('Please run costngn-cli list-profiles to see all available profiles')
        quit()

    
@app.callback(invoke_without_command=True)
def foo():
    version = pkg_resources.require("costngn-cli")[0].version
    typer.echo(colored(f'Welcome to costngn-cli {version} (alpha)','yellow'))
    #typer.echo(f"{__app_name__} v{__version__}")
    global config_file
    config_file=os.path.join(Path.home(), 'costngn','.config','config.toml')
    global result_path
    result_path=os.path.join(Path.home(), 'costngn','results')
    #typer.echo(f"{lat}, {long}, {method}")

@app.command()
def config():
    """
    Input and store your account access information
    """
    #global config_file
    #config_file=os.path.join(Path.home(), 'costngn','config.toml')
    typer.echo('Enter below your account access information:')
    typer.echo('It will be saved into config file')
    #typer.run(conf_main,config_file)
    conf_main(config_file)

@app.command()
def list_profiles():
    """
    Show your stored account/s access information
    """
    typer.echo('Show config file content:')
    #typer.run(conf_show(),config_file)
    conf_show(config_file)

@app.command()
def aws(nick:str):
    """
    Gets AWS instances data - 'costngn-cli aws --help' for options
    """
    company='aws'
    #nick=choose_acc(company)
    #typer.echo(f'Go to {company.upper()} data:')
    
    nick_ok(company, nick)
    #typer.run(aws_main)
    #cost=False
    #duration = time.time() - start_time; print(f"It took {round(duration,4)} seconds")
    #start_time = time.time()
    rep=aws_main(nick,config_file)
    
    #if graph: rep_gtable(nick, rep, company)
    rep_table(nick, rep, company)

@app.command()
def do(nick:str):

    """
    Gets Digital Ocean instances data \n 'costngn-cli do --help' for options
    """
    company='do'
    #nick=choose_acc(company)
    nick_ok(company, nick)
    #typer.echo(f'Go to {company.upper()} data:')
    rep= do_main(company, nick,config_file,result_path)
    #if graph: rep_gtable(nick, rep, company)
    rep_table(nick, rep, company)

@app.command()
def het(nick:str):

    """
    Gets Hetzner instances data \n 'costngn-cli het --help' for options
    """
    company='het'
    #nick=choose_acc(company)
    nick_ok(company, nick)
    #typer.echo(f'Go to {company.upper()} data:')
    rep= het_main(company, nick,config_file,result_path)
    #if graph: rep_gtable(nick, rep, company)
    rep_table(nick, rep, company)

@app.command()
def lin(nick:str):
    """
    Gets Linode instances data \n 'costngn-cli lin --help' for options
    """
    company='lin'
    #nick=choose_acc(company)
    nick_ok(company, nick)
    #typer.echo(f'Go to {company.upper()} data:')
    rep= lin_main(company, nick,config_file,result_path)
    #if graph: rep_gtable(nick, rep, company)
    rep_table(nick, rep, company)


@app.command()
def remove(nick:str):
    """
    Remove given profile_id account from config file
    """
    #nick_ok(company, nick)
    #typer.echo(f'Go to {company.upper()} data:')
    conf_del(nick,config_file)




if __name__ == "__main__":
    app()
    



