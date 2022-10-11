cd Custom-Flower/App

tmux new-session -d -s custom-flower-app;

tmux split-window;
tmux split-window -h;

tmux send-keys -t 0 p y t h o n 3 \  s e r v e r . p y;
tmux send-keys -t 1 p y t h o n 3 \  c l i e n t . p y;
tmux send-keys -t 2 p y t h o n 3 \  c l i e n t . p y;
tmux select-pane -t 0;

tmux a;
