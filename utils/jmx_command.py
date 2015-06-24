from config import get_confd_path
from jmxfetch import JMXFetch, JMX_LIST_COMMANDS
from util import get_os


def jmx_command(args, agent_config, redirect_std_streams=False):
    """
    Run JMXFetch with the given command if it is valid (and print user-friendly info if it's not)
    """
    if len(args) < 1 or args[0] not in JMX_LIST_COMMANDS.keys():
        print "#" * 80
        print "JMX tool to be used to help configuring your JMX checks."
        print "See http://docs.datadoghq.com/integrations/java/ for more information"
        print "#" * 80
        print "\n"
        print "You have to specify one of the following commands:"
        for command, desc in JMX_LIST_COMMANDS.iteritems():
            print "      - %s [OPTIONAL: LIST OF CHECKS]: %s" % (command, desc)
        print "Example: sudo /etc/init.d/datadog-agent jmx list_matching_attributes tomcat jmx solr"
        print "\n"

    else:
        jmx_command = args[0]
        checks_list = args[1:]
        confd_directory = get_confd_path(get_os())

        jmx_process = JMXFetch(confd_directory, agent_config)
        jmx_process.configure()
        should_run = jmx_process.should_run()

        if should_run:
            jmx_process.run(jmx_command, checks_list, reporter="console", redirect_std_streams=redirect_std_streams)
        else:
            print "Couldn't find any valid JMX configuration in your conf.d directory: %s" % confd_directory
            print "Have you enabled any JMX check ?"
            print "If you think it's not normal please get in touch with Datadog Support"
