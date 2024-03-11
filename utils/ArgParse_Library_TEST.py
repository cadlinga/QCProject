import argparse

#Setup argparse (Command Line Interface): 
parser = argparse.ArgumentParser(description='Description: This program adds numbers.')

#Create each argument/variable we'd like to specify in CLI.
parser.add_argument('x', metavar='x', type=int, help='Enter integer x-value')
parser.add_argument('y', metavar='y', type=int, help='Enter integer y-value')

#OPTIONAL: create an optional command to type into the CLI 
#(can be used as a flag or specific choice).
parser.add_argument('-d', '--details', help='Gives additional details of operation.',
                    action='store_true', required=False)

parser.add_argument('-o', '--option', help='Choose an option for the code.',
                    type=int, choices=[0, 1, 2], default=0, nargs='?')
#-> not specifying the "option" argument in the CLI makes it use the default value specified.
#-> Setting a default also requires to specify hwo many arguments it needs to look for with "nargs". '?'->1
#-> Note that since we set a "default", we don't need "required=False" anymore (redundant).

#Make the above arguments/variables retrievable for use in our code.
args = parser.parse_args()

x = args.x
y = args.y
details = args.details
option = args.option

#Write some code that uses x, y and the optional command "details":
def operation(x, y):
    return(x + y)

if details:
    print('Detailed output:', x, '+', y, '=', operation(x, y))
else:
    print(operation(x, y))

print('Code running with OPTION', option)


#COMMANDS in CMD+CLI:
#cd C:\Users\Predator\source\repos\ArgParse Library TEST\
#python ArgParse_Library_TEST.py 20 30 -d -o 1

# -h -> lists defined arguments & associated help strings.
