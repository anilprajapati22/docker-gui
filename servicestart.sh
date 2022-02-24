#!/bin/bash

echo "<h1> sgn ons jkh jam jbm jkh jcs jjb jam jom jsm jlm jsm jgb jsm jkb jgb jgb jjb jd jd jd jmp jg jrm jsp: </br> $(hostname -f)</h1>" > index.html
/usr/sbin/apache2 -D FOREGROUND

