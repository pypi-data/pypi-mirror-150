.. _genocide:

.. raw:: html

    <br>


.. title:: genocide


.. raw:: html

    <br>

.. image:: skulllinesmall3.jpg
    :width: 100%
    :height: 2.2cm
    :target: reconsider.html

.. raw:: html

    <br><br>


**NAME**

 **GENOCIDE** - Prosecutor. Reconsider. OTP-CR-117/19. 


**SYNOPSIS**


 | ``sudo genocidectl <cmd> [key=value] [key==value]``


**DESCRIPTION**

 **GENOCIDE** is a solid, non hackable bot, that runs under systemd as a 
 24/7 background service starts after reboot and is intended to be programmable
 in a static, only code, no popen, no user imports and no reading modules from
 a directory, way. It can show genocide and suicide stats of king netherlands
 his genocide into a IRC channel, display rss feeds and log simple text
 messages. Source code is :ref:`here <source>`.

 **GENOCIDE** holds evidence that king netherlands is doing a genocide, a 
 written :ref:`response <guilty>` where king netherlands confirmed taking note
 of “what i have written”, namely :ref:`proof <evidence>` that medicine he
 uses in treatement laws like zyprexa, haldol, abilify and clozapine are poison
 that make impotent, is both physical (contracted muscles) and mental (let 
 people hallucinate) torture and kills members of the victim groups. 

 **GENOCIDE** contains :ref:`correspondence <correspondence>` with the
 International Criminal Court, asking for arrest of the king of the 
 netherlands, for the genocide he is committing with his new treatement laws.
 Current status is an outside the jurisdiction judgement of the prosecutor 
 which requires a :ref:`reconsider <reconsider>` to have the king actually
 arrested.


**INSTALL**


 | $ ``sudo pip3 install genocide --upgrade --force-reinstall``


**CONFIGURATION**


 **irc**

 | $ ``sudo genocidectl cfg server=<server> channel=<channel> nick=<nick>``
 |
 | (*) default channel/server is #genocide on localhost

 **sasl**

 | $ ``sudo genocidectl pwd <nickservnick> <nickservpass>``
 | $ ``sudo genocidectl cfg password=<outputfrompwd>``

 **users**

 | $ ``sudo genocidectl cfg users=True``
 | $ ``sudo genocidectl met <userhost>``

 **24/7**

 | $ ``sudo cp /usr/local/share/genocide/genocide.service /etc/systemd/system``
 | $ ``sudo systemctl enable genocide --now``


**COMMANDS**


 | ``cmd`` - shows all commands
 | ``cfg`` - shows the irc configuration, also edits the config
 | ``dlt`` - removes a user from genocide
 | ``dpl`` - sets display items for a rss feed
 | ``ftc`` - runs a rss feed fetching batch
 | ``fnd`` - allows you to display objects on the datastore, read-only json files on disk 
 | ``flt`` - shows a list of instances registered to the bus
 | ``log`` - logs some text
 | ``mdl`` - genocide model
 | ``met`` - adds a users with there irc userhost
 | ``mre`` - displays cached output, channel wise.
 | ``nck`` - changes nick on irc
 | ``now`` - show genocide stats
 | ``ops`` - tries to give you operator status (+o)
 | ``pwd`` - combines a nickserv name/password into a sasl password
 | ``rem`` - removes a rss feed by matching is to its url
 | ``req`` - request to the prosecutor
 | ``rss`` - adds a feed to fetch, fetcher runs every 5 minutes
 | ``slg`` - slogan
 | ``sts`` - suidicde stats
 | ``thr`` - show the running threads
 | ``tpc`` - set genocide stats in topic
 | ``trt`` - torture definition
 | ``wsd`` - wisdom


**FILES**


 | ``/usr/local/share/doc/genocide/*``
 | ``/usr/local/share/genocide/genocide.service``


**SEE ALSO**

 | http://genocide.rtfd.io
 | http://pypi.org/project/genocide

**COPYRIGHT**

 **GENOCIDE** is placed in the Public Domain. No Copyright, No License.

**AUTHOR**

 Bart Thate 

.. toctree::
    :hidden:
    :glob:

    reconsider
    evidence
    guilty
    source
    correspondence
    zadmin
