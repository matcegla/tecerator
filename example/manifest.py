import tecerator as tc

symbol = 'add'
title = 'Addition'
author = 'Mateusz Cegiełka'
author_id = 'pustaczek'
author_email = 'mateusz@cegla.net'
contest = 'Tecerator Example 2019'
date = '17.05.2019'
description = './desc.tex'
time_limit = 2 * tc.unit.SECOND
memory_limit = 64 * tc.unit.MEGABYTE
solutions = [
    tc.Solution.good('./main.cpp'),
]
tests = [
    tc.Group.example([
        tc.Test.hardcoded('./0.in'),
    ]),
    3 * tc.Test('./gen.cpp'),
    3 * tc.Test('./gen.cpp'),
    3 * tc.Test('./gen.cpp'),
]
