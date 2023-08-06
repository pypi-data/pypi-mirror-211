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

export type IJupyterEducation = {
  timer: Timer,
  TimerView: (props: ITimerViewProps) => JSX.Element,
};

export const IJupyterEducation = new Token<IJupyterEducation>(
  '@datalayer/jupyter-education:plugin'
);

export const jupyterDocker: IJupyterEducation = {
  timer,
  TimerView,
}

/**
 * The command IDs used by the jupyter-education-widget plugin.
 */
namespace CommandIDs {
  export const create = 'create-jupyter-education-widget';
}

/**
 * Initialization data for the @datalayer/jupyter-education extension.
 */
const plugin: JupyterFrontEndPlugin<IJupyterEducation> = {
  id: '@datalayer/jupyter-education:plugin',
  autoStart: true,
  requires: [ICommandPalette],
  optional: [ISettingRegistry, ILauncher],
  provides: IJupyterEducation,
  activate: (
    app: JupyterFrontEnd,
    palette: ICommandPalette,
    settingRegistry: ISettingRegistry | null,
    launcher: ILauncher
  ): IJupyterEducation => {
    const { commands } = app;
    const command = CommandIDs.create;
    commands.addCommand(command, {
      caption: 'Show Jupyter Education',
      label: 'Jupyter Education',
      icon: (args: any) => reactIcon,
      execute: () => {
        const content = new DatalayerWidget();
        const widget = new MainAreaWidget<DatalayerWidget>({ content });
        widget.title.label = 'Jupyter Education';
        widget.title.icon = reactIcon;
        app.shell.add(widget, 'main');
      }
    });
    const category = 'Jupyter Education';
    palette.addItem({ command, category, args: { origin: 'from palette' } });
    if (launcher) {
      launcher.add({
        command,
        category: 'Datalayer',
        rank: -1,
      });
    }
    console.log('JupyterLab extension @datalayer/jupyter-education is activated!');
    if (settingRegistry) {
      settingRegistry
        .load(plugin.id)
        .then(settings => {
          console.log('@datalayer/jupyter-education settings loaded:', settings.composite);
        })
        .catch(reason => {
          console.error('Failed to load settings for @datalayer/jupyter-education.', reason);
        });
    }
    requestAPI<any>('get_example')
      .then(data => {
        console.log(data);
      })
      .catch(reason => {
        console.error(
          `The jupyter_education server extension appears to be missing.\n${reason}`
        );
      });
    connect('ws://localhost:8888/jupyter_education/echo', true);
    return jupyterDocker;
  }
};

export default plugin;
