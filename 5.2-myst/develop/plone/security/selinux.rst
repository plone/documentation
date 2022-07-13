========================
Using SELinux with Plone
========================

.. admonition:: Description

    Tutorial on using SELinux with Plone, using Plone 4.3 and RedHat Linux 6.3.


Introduction
============

This document is a tutorial on using SELinux with Plone, using RedHat Linux 6.3 and Plone 4.3. It is applicable to any Linux distribution with small changes.

About SELinux
=============

SELinux is a mandatory access control system, meaning that SELinux assigns security *contexts* (presented by *labels*) to system resources, and allows access only to the processes that have defined required levels of authorization to the contexts. In other words, SELinux maintains that certain *target* executables (having security contexts) can access (level of access being defined explicitly) only certain files (having again security context labels). In essence the contexts are roles, which makes SELinux a Role Based Access Control system. It should be noted that even root is usually just an ordinary user for RBAC systems, and will be contained like any other user.

The concept of contexts and labels can be slightly confusing at first. It stems from the idea of chain of trust. A system that upholds that proper authorization checks are being done is worthless if the system allows moving the protected data to a place that does not have similar authorization checks. Context labels are file system attributes, and when the file is moved around the label (representing context) moves with the file. The system is supposed to limit where the information can be moved, and the contexts can be extended beyond file system (ie. labels on rows in database systems), building complete information systems that will never hand over data to a party that is unable (or unwilling) to take care of it.

Most SELinux policies *target* an executable, and define the contexts (usually applied with labels to files) it can access by using *type enforcement rules*. However there are also *capabilities* that control more advanced features such as the ability to execute heap or stack, setuid, fork process, bind into ports, or open TCP sockets. Most of the capabilities and macros come from reference policy, which offers policy developers ready solutions to most common problems. The reference policy shipped by Linux distributions contains ready rules for some 350 targets, including applications like most common daemons (sshd), and system services (init/systemd).

The value of SELinux is in giving administrators fine granularity of access control far beyond the usual capabilities of \*NIX systems. This is useful especially in mitigating the impact of security vulnerabilities. The most apparent downside to SELinux is the high skill requirements. To understand most of SELinux - and to be able to maintain it effectively with 3rd party applications - requires good abstraction skills, and especially the official documentation is somewhat hard to digest. SELinux was never engineered to be easy for administrators. It was engineered to be able to implement complex security models like Bell-LaPadula and MLS.

There have been several myths about SELinux being heavy (in reality it comes with ~3% overhead), or that it breaks all applications. There used to be time (years ago) when SELinux applied itself by default on everything, and if the application was not included in the shipped policies it probably failed miserably. Most of the application developers and companies got frustrated to the situation, and started recommending that SELinux should always be disabled. Things have luckily changed drastically since then. Today most SELinux implementations use what is called *targeted policy*, which means that SELinux affects only applications that have explicit policies. As a result SELinux does generally nothing to your 3rd party applications - good or bad - until you enable it. This tutorial is meant to give readers pointers on how to accomplish exactly that.

Creating new SELinux policy
===========================

Prerequisities
--------------

- root access
- Working SELinux (*sudo sestatus* reports **ENABLED**, and **enforcing**)
- Preferably a system that uses *targeted policy* (see the output of previous command)
- SELinux policy utilities installed (policycoreutils-python policycoreutils-gui)
- The application (in this case Plone) already installed

Creating new policy
-------------------

Development starts usually by generating a policy skeleton with the *sepolgen* (or sepolicy-generate) utility. It can generate several types of templates, which come with a set of basic access rights. There are several sepolgen versions out there, depending on the Linux distribution. The most important differences between them are in the included templates. Creating new policy is done with the following command: ::

    sepolgen -n plone -t 3 /usr/local/Plone/zinstance/bin/plonectl

Where the parameters are:

- **-n plone** gives the new policy name. Default is to use the name of the executable, but we want to give a more generic name in this case.
- **-t 3** elects a template ("*normal application*") that gives some commonly required access rights as a starting point
- **/usr/local/Plone/zinstance/bin/plonectl** is the application that will get a new context (*plonectl_exec_t*), which will get most of the type enforcement rules.

The outcoming result will be four files:

- **plone.te** Type enforcement file defining the access rules. **This file contains most of the policy, and most of the rules go there.**
- **plone.if** Interface file defining what *other* policies can import from your policy.
- **plone.fc** File contexts file defining what context labels will be applied to files and directories.
- **plone.sh** Setup script that will compile and install the policy to the system configuration (both running and persistent).

Labeling files
--------------

Before the actual development will start file context labeling rules should be defined in **plone.fc**. You probably need some context (*plone_t*) for all files related to Plone, context (*plone_rw_t*) with write rights to *var* and the plonectl will need a context (*plonectl_exec_t*) that comes with special rights. ::

    /usr/local/Plone(.*) gen_context(system_u:object_r:plone_t,s0)
    /usr/local/Plone/zinstance/var(.*) gen_context(system_u:object_r:plone_rw_t,s0)
    /usr/local/Plone/zinstance/bin/plonectl gen_context(system_u:object_r:plonectl_exec_t,s0)

The generated **plone.te** already tells SELinux what *plone_t* and *plone_exec_t* are - valid file context types. The tools labeling files will know what to do about them. However the *plone_rw_t* is must be introduced before continuing, and the plone_t should be renamed to *plonectl_t* (to describe the target better - important for managing more complex rules): ::

    type plonectl_exec_t;
    application_domain(plone_t, plonectl_exec_t)
    type plone_rw_t;
    files_type(plone_rw_t)

It is also a good idea to edit the restorecon commands at the end of **plone.sh** to point to /usr/local/Plone and relabel all the files when the policy is recompiled and installed: ::

    /sbin/restorecon -F -R -v /usr/local/Plone

Development process
===================

The basic policy development process for SELinux policies follows the following pattern:

#. Add permissive rules
#. Compile & install your policy
#. Clear the audit logs
#. Run the application until it fails
#. Run audit2allow
#. Study the output of audit2allow, and add more access rules to satisfy the application
#. Repeat from step 2 until everything works
#. Remove permissive rules

Permissive rules
----------------

Most applications require largish amount of rules just to start properly. To reach a working set of rules faster you can switch your contexts to permissive mode by editing the *PlonePython.te*: ::

    require {
        type unconfined_t;
    }

    permissive plone_t;
    permissive plonectl_exec_t;
    permissive plone_rw_t;

Permissive in SELinux means that all actions by mentioned contexts will be allowed to process, and the incidents (*access vector denials*) will be only logged. This will allows to gather rules faster than going through the complete development cycle.

.. warning::
   Please note that permissive rules have to be removed at some point, or the policy will **not** protect the application as expected.

Using audit2allow
-----------------

Audit2allow can search both dmesg and the system audit logs for access vector cache denials, and build suggestions based on them. Because the output will be more understandable without extra noise, it is recommendable to clear audit log between development cycles. Since it is probably not a good idea to clear dmesg, it is suggested that you clear the system audit logs, and instruct audit2allow to use them as source, for example: ::

    cat /dev/null > /var/log/audit.log
    # Break the application
    audit2allow -r -R -i /var/log/audit/audit.log

There are couple useful parameters for running audit2allow:

- *-r* adds requires ("imports" from other policies) to the output
- *-R* makes audit2allow suggest compatible macros from other available policies. Macros contain often more lenient access rules, but they also reduce the amount of required rules. Using them will make the policy slightly more platform dependent, but easier to maintain.
- *-i /var/log/audit/audit.log* makes only to audit logs to be evaluated for rules

.. tip::
   Always when in trouble, and you suspect access vector cache denial, use audit2allow. If you can't figure out what is going on, also check out the output of *audit2why*, similar tool that produces more human readable reasons why access was denied. Beware though, audit2why is somewhat heavy.

Example type enforcement rules
------------------------------

SELinux rules are actually quite simple. For instance the following rule tells to *allow* the process that has context *plonectl_exec_t* access to most common temporary files (*tmp_t*, defined in the reference policy), and the level of access will allow it most of the things that are usually done to files (but not all, for instance *setattr* is missing): ::

    allow plonectl_exec_t tmp_t:file { write execute read create unlink open getattr };

For the previous to be usable the *tmp_t* and *file* have to be introduced to the compiler, that will search for them from the other available policies. Type is a grouping item that will usually point to a security context (labeled files), while classes define what access types (ie. getattr) can are available for the type. The term *type enforcement rule* comes from the fact that SELinux rules define who can do what to the objects that are linked to types. ::

    requires {
      type tmp_t { write execute read create unlink open getattr };
      class file;
    }

There are also macros that will help in accomplishing more complex tasks. The following macro will give the executable right to bind to 8080/TCP: ::

    corenet_tcp_bind_transproxy_port(plonectl_exec_t)

To get an idea about what items are available the `Reference policy API documentation <http://oss.tresys.com/docs/refpolicy/api/>`_ is the place go to.

Caveats
-------

First of all, audit2allow is not a silver bullet. There are cases where your application accesses something that it does not really require for operation, for instance to scan your system for automatic configuration of services. There are also cases where it prints nothing yet the application clearly is denied access to something. That can be caused by *dontaudit* rules, which silence logging of events that could generate too much noise. In any case a healthy amount of criticism should be applied to everything audit2allow output, especially when the suggested rules would give access rights to outside application directories.

Misconfiguration can cause either file labeling to fail, or the application process not to get transitioned to proper executing context. If it seems that the policy is doing nothing, check that the files are labeled correctly (`ls -lFZ`), and the process is running in the correct context (`ps -efZ`).

Evaluating the file context rules (fules and their labels) is managed by a heurestic algorithm, which gives precedence to more specific rules by evaluating the length and precision of the path patterns. The patterns are easy for beginner to misconfigure. When suspecting that the file context rules are not getting applied correctly, always investigate `semanage fcontext -l` to see what rules match your files.

Policies for Plone
==================

The following contains results of ordinary "install, test & break, add rules, repeat from beginning" development cycle for a basic Plone SELinux policy.

Relabeling rights
-----------------

By default you might not have the right to give any of new security labels to files, and *restorecon* may throw permission denied errors. To give the SELinux utilities (using the context *setfiles_t*) the right to change the security context based on the new types add the following rules: ::

    require {
        type setfiles_t;
        type fs_t;
        class lnk_file relabelto;
        class dir relabelto;
        class lnk_file relabelto;
    }

    allow plone_t fs_t:filesystem associate;
    allow setfiles_t plone_t:dir relabelto;
    allow setfiles_t plone_t:file relabelto;
    allow setfiles_t plone_t:lnk_file relabelto;
    allow setfiles_t plonectl_exec_t:dir relabelto;
    allow setfiles_t plonectl_exec_t:file relabelto;
    allow setfiles_t plonectl_exec_t:lnk_file relabelto;
    allow setfiles_t plone_rw_t:dir relabelto;
    allow setfiles_t plone_rw_t:file relabelto;
    allow setfiles_t plone_rw_t:lnk_file relabelto;
    # Python interpreter creates pyc files, this is required to relabel them correctly in some cases
    allow setfiles_t plone_t:file relabelfrom;

If the transition is not done, the application will keep running in the starting user's original context. Most likely that will be unconfined_t, which means no SELinux restrictions will be applied to the process.

Transition to context
---------------------

When you first run Plone (ie. "plonectl fg"), you will notice that it doesn't run, complaining about bad interpreter. Audit2allow will instruct to give rights to your uncontained_t context to run the python interpreter. This is however wrong. You wish to first instruct SELinux to change the process always to the new context (*plonectl_exec_t*) when the application is run. You also wish to have the necessary rights to execute the application so that the context transition can start: ::

    require {
      type unconfined_t;
      class process { transition siginh noatsecure rlimitinh };
    }
    # unconfined_r user roles have access to plonectl_exec_t
    role unconfined_r types plonectl_exec_t;
    # unconfined process contexts should also have execution rights to the python executable etc
    allow unconfined_t plone_t:file execute;

    # When unconfined_t runs something that has plonectl_exec_t transition the execution context to it
    type_transition unconfined_t plonectl_exec_t:process plonectl_exec_t;
    # Allow the previous, and some basic process control
    allow unconfined_t plonectl_exec_t:process { siginh rlimitinh noatsecure transition };
    # The new process probably should have rights to itself
    allow plonectl_exec_t self:file entrypoint;

Later when enough rules are in place for the application to run take a look at the process context to see that the transitioning to *plonectl_exec_t* works: ::

    # ps -efZ|grep python
    unconfined_u:unconfined_r:plonectl_exec_t:s0-s0:c0.c1023 root 1782 1  0 16:32 ? 00:00:00 /usr/local/Plone/Python-2.7/bin/python ...
    unconfined_u:unconfined_r:plonectl_exec_t:s0-s0:c0.c1023 500 1784 1782  8 16:32 ? 00:00:07 /usr/local/Plone/Python-2.7/bin/python ...

Common process requirements
---------------------------

In order for any \*NIX process to work some basic requirements must be met. Applications require for instance access to /dev/null, and PTYs: ::

    dev_rw_null(plonectl_exec_t)
    domain_type(plonectl_exec_t)
    files_list_root(plonectl_exec_t)
    unconfined_sigchld(plonectl_exec_t)
    dev_read_urand(plonectl_exec_t)
    userdom_use_inherited_user_ptys(plonectl_exec_t)
    miscfiles_read_localization(plonectl_exec_t)

Zope/PLONE
------------------

After running the plonectl commands (fg, start, stop) several times, and adding the required rules you should end up with something like following. First you will have a large amount of require stanzas for the rule compiler, and then an intermediate amount of rules: ::

    require {
      class dir { search read create write getattr rmdir remove_name open add_name };
      class file { rename setattr read lock create write getattr open append };
      type tmp_t;
    }

    # Read access to common Plone files
    allow plonectl_exec_t plone_t:dir { search read open getattr add_name };
    allow plonectl_exec_t plone_t:file { execute read create getattr execute_no_trans ioctl open };
    allow plonectl_exec_t plone_t:lnk_file { read getattr };

    # Read/write access rights to var and temporary files
    allow plonectl_exec_t plone_rw_t:dir { search unlink read create write getattr rmdir remove_name open add_name };
    allow plonectl_exec_t plone_rw_t:file { unlink rename setattr read lock create write getattr open append };
    allow plonectl_exec_t tmp_t:file { unlink rename execute setattr read create write getattr unlink open };
    allow plonectl_exec_t tmp_t:dir add_name;
    fs_search_tmpfs(plonectl_exec_t)
    fs_manage_tmpfs_dirs(plonectl_exec_t)
    fs_manage_tmpfs_files(plonectl_exec_t)
    allow plonectl_exec_t tmpfs_t:file execute;
    files_delete_tmp_dir_entry(plonectl_exec_t)

    # Networking capabilities
    allow plonectl_exec_t self:netlink_route_socket { write getattr read bind create nlmsg_read };
    allow plonectl_exec_t self:tcp_socket { setopt read bind create accept write getattr getopt listen };
    allow plonectl_exec_t self:udp_socket { write read create ioctl connect };
    allow plonectl_exec_t self:unix_stream_socket { create connect };
    corenet_tcp_bind_generic_node(plonectl_exec_t)
    corenet_tcp_bind_http_cache_port(plonectl_exec_t)

    # Ability to fork to background, and to communicate with child processes via socket
    allow plonectl_exec_t self:process { fork sigchld };
    allow plonectl_exec_t plone_rw_t:sock_file { create link write read unlink setattr };
    allow plonectl_exec_t self:unix_stream_socket connectto;
    allow plonectl_exec_t self:capability { setuid setgid };

    # Rights to managing own process
    allow plonectl_exec_t self:capability { kill dac_read_search dac_override };
    allow plonectl_exec_t self:process { signal sigkill };

Gathering the previous audit2allow failed completely to report tcp_socket read and write. Some system policy had probably introduced a *dontaudit* rule, which quiesced the logging for that access vector denial. Luckily Plone threw out very distinct Exception, which made resolving the issue easy.

ZEO
---

There are couple differences between standalone and ZEO installations. To support both a boolean is probably good way to go. Booleans can be managed like: ::

    # getsebool ploneZEO
    ploneZEO --> off
    # setsebool ploneZEO=true
    # setsebool ploneZEO=false

Installing Plone in ZEO mode will change the directory *zinstance* to *zeocluster*. It is alright to either have both defined in **plone.fc**, or to use regexp: ::

    /usr/local/Plone/zeocluster/var.* gen_context(system_u:object_r:plone_rw_t,s0)
    # or
    /usr/local/Plone/(zinstance|zeocluster)/var.* gen_context(system_u:object_r:plone_rw_t,s0)

The differences to type enforcement policy consist mostly of more networking abilities (which one probably should not allow unless really required), and the ability to run shells (ie. bash): ::

    require {
      type bin_t;
      type shell_exec_t;
    }

    # ZEO
    bool ploneZEO false;
    if (ploneZEO) {
    allow plonectl_exec_t plone_t:file execute_no_trans;
    allow plonectl_exec_t self:tcp_socket connect;
    corenet_tcp_bind_transproxy_port(plonectl_exec_t)
    nis_use_ypbind_uncond(plonectl_exec_t)
    # Starting ZEO requires running shells
    kernel_read_system_state(plonectl_exec_t)
    allow plonectl_exec_t shell_exec_t:file { read open execute };
    }

Maintenance utilities
---------------------

The procedure for allowing maintenance utilities like *buildout* to work is quite straight forward. First introduce a new context: ::

    type plone_maint_exec_t;
    files_type(plone_maint_exec_t)

Then label the maintenance utilities using the context: ::

    /usr/local/Plone/zinstance/bin/buildout gen_context(system_u:object_r:plone_maint_exec_t,s0)

Last, provide the necessary rules for relabeling, context transition, and for the process to run without any restrictions: ::

    role unconfined_r types plone_maint_exec_t;
    allow unconfined_t plone_maint_exec_t:file execute;
    type_transition unconfined_t plone_maint_exec_t:process plone_maint_exec_t;
    allow unconfined_t plone_maint_exec_t:process { siginh rlimitinh noatsecure transition };
    allow plone_maint_exec_t self:file entrypoint;

    # Allow anything labeled plone_mait_exec_t to do basically anything
    permissive plone_maint_exec_t;

After running maintenance tasks you should make sure the files have still correct labels by running something like: ::

    /sbin/restorecon -F -R /usr/local/Plone

.. tip::
   See also "setenforce Permissive", which will disable enforcing SELinux rules temporarily system wide.

Testing the policy
==================

Easiest way to test the policy is to label for instance the Python executable as plone_exec_t by using *chcon*, and to test the policy using Python scripts. For example: ::

    # cd /usr/local/Plone/Python2.7/bin
    # setenforce Permissive
    # chcon system_u:object_r:plonectl_exec_t:s0 python2.7
    # setenforce Enforcing
    # ./python2.7
    Python 2.7.3 (default, Apr 28 2013, 22:22:46)
    [GCC 4.4.7 20120313 (Red Hat 4.4.7-3)] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import os
    >>> os.listdir('/root')
    Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
    OSError: [Errno 13] Permission denied: '/root'
    >>> # That should have worked, running python interpreter as root and all
    >>> exit()
    # setenforce Permissive
    # chcon system_u:object_r:plonectl_t:s0 python2.7
    # setenforce Enforcing

This can be refined into automated testing. Other forms such as Portlet inside running Plone process can also be used for testing.

Deploying the policy
====================

SELinux policies can be installed simply by running *semodule -n -i <compiled_policy.pp>*. In case packaging is required (for rolling out Plone instances automatically, or for use with centralized management tools like Satellite) it is easy to accomplish with rpm. In order to do that first install the rpm building tools: ::

    yum install rpm-build

Then modify the following RPM spec file to suit your needs: ::

    %define relabel_files() \
    restorecon -R /usr/local/Plone; \

    %define selinux_policyver 3.7.19-195

    Name:   plone_selinux
    Version:    1.0
    Release:    1%{?dist}
    Summary:    SELinux policy module for plone

    Group:  System Environment/Base
    License:    GPLv2+
    # This is an example. You will need to change it.
    URL:        http://setest
    Source0:    plone.pp
    Source1:    plone.if

    Requires: policycoreutils, libselinux-utils
    Requires(post): selinux-policy >= %{selinux_policyver}, policycoreutils
    Requires(postun): policycoreutils
    Requires(post): python
    BuildArch: noarch

    %description
    This package installs and sets up the  SELinux policy security module for plone.

    %install
    install -d %{buildroot}%{_datadir}/selinux/packages
    install -m 644 %{SOURCE0} %{buildroot}%{_datadir}/selinux/packages
    install -d %{buildroot}%{_datadir}/selinux/devel/include/contrib
    install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/selinux/devel/include/contrib/

    %post
    semodule -n -i %{_datadir}/selinux/packages/plone.pp
    if /usr/sbin/selinuxenabled ; then
        /usr/sbin/load_policy
        %relabel_files
    fi;
    exit 0

    %postun
    if [ $1 -eq 0 ]; then
        semodule -n -r plone
        if /usr/sbin/selinuxenabled ; then
           /usr/sbin/load_policy
           %relabel_files
        fi;
    fi;
    exit 0

    %files
    %attr(0600,root,root) %{_datadir}/selinux/packages/plone.pp
    %{_datadir}/selinux/devel/include/contrib/plone.if

    %changelog
    * Wed May  1 2013 YOUR NAME <YOUR@EMAILADDRESS> 1.0-1
    - Initial version

The rpm packages will be built by running the rpmbuild: ::

    # rpmbuild -ba plone.spec
    # ls -lF /root/rpmbuild/RPMS/noarch/
    -rw-r--r--. 1 root root 17240  1.5. 19:24 plone_selinux-1.0-1.el6.noarch.rpm

External resources
==================

The following external resources are sorted by probable usefulness to someone who is beginning working with SELinux:

- `Fedora SELinux FAQ <https://docs.fedoraproject.org/en-US/Fedora/13/html/SELinux_FAQ/index.html>`_
- `Reference policy API <http://oss.tresys.com/docs/refpolicy/api/>`_
- `NSA - SELinux FAQ <http://www.nsa.gov/research/selinux/faqs.shtml>`_
- `NSA - SELinux main website <http://www.nsa.gov/research/selinux/index.shtml>`_
- `Official SELinux project wiki <http://selinuxproject.org/>`_
- `Red Hat Enterprise SELinux Policy Administration (RHS429) classroom course <https://www.redhat.com/training/courses/rhs429/>`_
- `Tresys Open Source projects <http://www.tresys.com/open-source.php>`_ (IDE, documentation about the reference policy, and several management tools)

