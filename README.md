Do you often find yourself in need of a simple calculator, and all you have
available to you is a Brocade or Cisco IOS router?  No longer will you
experience the horror and dread of mental arithmetics. The route-map calculator
is here!


Brocade   : calculator-route-map.brocade.txt
Cisco IOS : calculator-route-map.ioscisco.txt
            (file size ~ 12 megabyte)


In general I don't find route-maps useful to accomplish, well, anything.
However, this is a striking example of re-usable configuration that has
a measurable impact on daily operations! 


Calculations can be performed with integers between 1 and 256. The
answer will be presented as a rounded positive integer. In case the
calculation would result in a negative integer, larger than 2^16
(65536), an helpful error message is generated: 65000:7777. For
divisions and substractions the order of the BGP communities is
relevant, one must always place the operator first!


arithmetic operators:

    'add' operator community:        65000:1
    'multiply' operator community:   65000:2
    'substract' operator community:  65000:3
    'divide' operator community:     65000:4


example output:
    
    telnet at input-router#show ip bgp routes detail 10.1.1.1 | i COMMUNITIES
                COMMUNITIES: 65000:2 0:63 0:113    ! calculate 63 * 113 
    telnet at input-router#

    telnet at calculator#show ip bgp routes detail 10.1.1.1 | i COMMUNITIES
              COMMUNITIES: 0:7119                ! result: 7119
    telnet at calculator#


Super convenient right?!


WARNING: due to IOS/Ironware architecture this route-map consumes quite
some memory. Always test in a lab before deploying in production!
