tmux new-session -d -s custom-flare-app;
tmux split-window -h;
tmux split-window;
tmux split-window -t 0;

tmux send-keys -t 0 . / p o c / s e r v e r / s t a r t u p / s t a r t . s h;
tmux send-keys -t 1 . / p o c / a d m i n / s t a r t u p / f l _ a d m i n . s h;
tmux send-keys -t 2 . / p o c / s i t e - 1 / s t a r t u p / s t a r t . s h;
tmux send-keys -t 3 . / p o c / s i t e - 2 / s t a r t u p / s t a r t . s h;
tmux select-pane -t 0;

tmux a;
