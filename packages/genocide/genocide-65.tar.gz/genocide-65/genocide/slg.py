# This file is placed in the Public Domain.


"""Prosecutor. Reconsider. OTP-CR-117/19."""


from hdl import Commands


txt1 = "@IntlCrimCourt @EU_ECHA @Europol @POL_DenHaag @Het_OM ask @KarimKhanQC to reconsider OTP-CR-117/19. #GGZ #ASP20 #ASP21"



def slg(event):
    event.reply(event.rest + " " + txt1)


Commands.add(slg)
