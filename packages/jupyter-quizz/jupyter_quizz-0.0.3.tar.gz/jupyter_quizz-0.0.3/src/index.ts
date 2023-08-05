import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { MainAreaWidget, ICommandPalette } from '@jupyterlab/apputils';
import { ILauncher } from '@jupyterlab/launcher';
import { reactIcon } from '@jupyterlab/ui-components';
import { Token } from '@lumino/coreutils';
import { DatalayerWidget } from './widget';
import { requestAPI } from './handler';
import { connect } from './ws';
import { timer, Timer, TimerView, ITimerViewProps } from "./store";

import '../style/index.css';

export type IJupyterQuizz = {
  timer: Timer,
  TimerView: (props: ITimerViewProps) => JSX.Element,
};

export const IJupyterQuizz = new Token<IJupyterQuizz>(
  '@datalayer/jupyter-quizz:plugin'
);

export const jupyterDocker: IJupyterQuizz = {
  timer,
  TimerView,
}

/**
 * The command IDs used by the jupyter-quizz-widget plugin.
 */
namespace CommandIDs {
  export const create = 'create-jupyter-quizz-widget';
}

/**
 * Initialization data for the @datalayer/jupyter-quizz extension.
 */
const plugin: JupyterFrontEndPlugin<IJupyterQuizz> = {
  id: '@datalayer/jupyter-quizz:plugin',
  autoStart: true,
  requires: [ICommandPalette],
  optional: [ISettingRegistry, ILauncher],
  provides: IJupyterQuizz,
  activate: (
    app: JupyterFrontEnd,
    palette: ICommandPalette,
    settingRegistry: ISettingRegistry | null,
    launcher: ILauncher
  ): IJupyterQuizz => {
    const { commands } = app;
    const command = CommandIDs.create;
    commands.addCommand(command, {
      caption: 'Show Jupyter Quizz',
      label: 'Jupyter Quizz',
      icon: (args: any) => reactIcon,
      execute: () => {
        const content = new DatalayerWidget();
        const widget = new MainAreaWidget<DatalayerWidget>({ content });
        widget.title.label = 'Jupyter Quizz';
        widget.title.icon = reactIcon;
        app.shell.add(widget, 'main');
      }
    });
    const category = 'Jupyter Quizz';
    palette.addItem({ command, category, args: { origin: 'from palette' } });
    if (launcher) {
      launcher.add({
        command,
        category: 'Datalayer',
        rank: -1,
      });
    }
    console.log('JupyterLab extension @datalayer/jupyter-quizz is activated!');
    if (settingRegistry) {
      settingRegistry
        .load(plugin.id)
        .then(settings => {
          console.log('@datalayer/jupyter-quizz settings loaded:', settings.composite);
        })
        .catch(reason => {
          console.error('Failed to load settings for @datalayer/jupyter-quizz.', reason);
        });
    }
    requestAPI<any>('get_example')
      .then(data => {
        console.log(data);
      })
      .catch(reason => {
        console.error(
          `The jupyter_quizz server extension appears to be missing.\n${reason}`
        );
      });
    connect('ws://localhost:8888/jupyter_quizz/echo', true);
    return jupyterDocker;
  }
};

export default plugin;
