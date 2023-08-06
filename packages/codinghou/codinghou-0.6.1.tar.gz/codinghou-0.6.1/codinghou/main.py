# -*- coding: utf-8 -*-
"""
 @Date    : 2021/2/3 21:51
 @Author  : Douglee
"""

from pyfiglet import Figlet, FigletFont


def greeting(font="larry3d"):
    f = Figlet(font=font)
    print(f.renderText('CODINGHOU'))
    print(f.renderText('Happy New Year'))


def get_fonts():
    """
    show all fonts
    :return:
    """
    all_fonts = FigletFont().getFonts()
    return all_fonts
