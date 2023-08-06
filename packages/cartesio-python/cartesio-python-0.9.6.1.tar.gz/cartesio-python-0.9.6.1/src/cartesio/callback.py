import os
from enum import Enum

from micromind.io.drive import Directory
from micromind.stamp import eventid

from cartesio.core.callback import Callback
from cartesio.enums import JSON_ELITE, JSON_HISTORY
from cartesio.utils.json_utils import write
from cartesio.utils.saving import JsonSaver
from cartesio.utils.stacking import GenerationStacker


class Event(Enum):
    START_STEP = "on_step_start"
    END_STEP = "on_step_end"
    START_LOOP = "on_loop_start"
    END_LOOP = "on_loop_end"


class CallbackVerbose(Callback):
    def _callback(self, n, e_name, e_content):
        fitness, time = e_content.get_best_fitness()
        fps = 1.0 / time
        if e_name == Event.END_STEP:
            verbose = f"[G {n:04}] {fitness:.4f} {time:.6f}s {int(round(fps))}fps"
            print(verbose)
        elif e_name == Event.END_LOOP:
            verbose = (
                f"[G {n:04}] {fitness:.4f} {time:.6f}s {int(round(fps))}fps, loop done."
            )
            print(verbose)


class CallbackSave(Callback):
    def __init__(self, workdir, dataset, frequency=1):
        super().__init__(frequency)
        self.workdir = Directory(workdir).next(eventid())
        self.dataset = dataset
        self.json_saver = None
        self.stacker = GenerationStacker()

    def set_decoder(self, decoder):
        super().set_decoder(decoder)
        self.json_saver = JsonSaver(self.dataset, self.decoder)

    def save_population(self, population, n):
        filename = f"G{n}.json"
        filepath = self.workdir / filename
        self.json_saver.save_population(filepath, population)

    def save_elite(self, elite):
        filepath = self.workdir / JSON_ELITE
        self.json_saver.save_individual(filepath, elite)

    def stack_files(self):
        generations = [
            f.path
            for f in os.scandir(self.workdir)
            if f.is_file() and f.name != JSON_ELITE and f.name != JSON_HISTORY
        ]
        history = self.stacker.stack(generations)
        filename = JSON_HISTORY
        filepath = self.workdir / filename
        write(filepath, history, indent=None)
        for generation in generations:
            os.remove(generation)

    def _callback(self, n, e_name, e_content):
        if e_name == Event.END_STEP or e_name == Event.END_LOOP:
            self.save_population(e_content.get_individuals(), n)
            self.save_elite(e_content.individuals[0])
