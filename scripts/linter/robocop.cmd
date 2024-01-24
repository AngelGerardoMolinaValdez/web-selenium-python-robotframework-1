@echo off
setlocal enabledelayedexpansion

mkdir "output/linter"

type nul > "./output/linter/robocop.log"

poetry run robocop
