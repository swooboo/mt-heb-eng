training_instructions.pdf: training_instructions.md
	cat $< |ssh sergey@tr.swooboo.com 'pandoc --from markdown -o /tmp/$@ ;cat /tmp/$@ ;rm /tmp/$@' >$@
send: training_instructions.pdf webserver_instructions.pdf
	bash -c 'echo $$1 attached |mailx -s $$1 -a $$1 $$USER' dummy $<
#bash -c 'echo Attached: \"$@\" |mailx -s \"Attachments: $@\" -a `echo $@ |sed \"s/ / -a /g\"` $USER' dummy $^

