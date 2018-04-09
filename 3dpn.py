%
% testing 3D PNG
% written by istaz@utm.my
% unit, metric
% 
%

clear all

% Define number of frames
nr_fr = 10;

% switches
use_avi=0;
use_axis=0;
use_frame=0;
use_plot=0;

% Initialize matrix using 'moviein'
if use_frame==1,
    frames = moviein(nr_fr);
end
if use_avi==1,aviobj = avifile('example.avi');end
% Generate frames with any plotting function.
% We use a cosine with variable frequency.
t = 0 : .01 : 6;
r2d=180/pi;
f = 1;
x1=20000;
y1=0;
z1=6000;
v1=200;
vx=1;
vy=0;
vz=0;
hdg1=45*pi/180;
pitch1=0*pi/180;
x2=0;
y2=0;
z2=0;
v2=800;
los=atan2(y1-y2,x1-x2);
losm=atan2(y1-y2,x1-x2);
losmold=0;
pitch=atan2(z1-z2,sqrt((x1-x2)^2+(y1-y2)^2));
miss=sqrt((x1-x2)^2+(y1-y2)^2+(z1-z2)^2);
png=4; % png ratio here
time=0;
i=0;
intercept=10; % interception radius, m
pngvalue=png;
ratio_min=99999;

if use_plot ==1
    fig=figure(10);
    clf;
end
losmrate_max=0;
lomsrate_time=999;
maxlosm=60.0*pi/180.0;
dt=0.01;
hold off
clf
while true
    i=i+1;
    %%%%%%%%%%
    % evader %
    %%%%%%%%%%
    asign=1;
    if rand>0.8, asign=-1;end
    if intercept*2 < miss,asign=6;end
    hdg1=rand*0*dt*pi/180*asign+hdg1;
    pitch1=2*dt*pi/180*asign+pitch1;
    x1=(v1*dt*cos(pitch1))*cos(hdg1)+x1;
    y1=(v1*dt*cos(pitch1))*sin(hdg1)+y1;
    z1=v1*dt*sin(pitch1)+z1;
    x1e=7000*cos(pitch1)*cos(hdg1)+x1;
    y1e=7000*cos(pitch1)*sin(hdg1)+y1;
    z1e=7000*sin(pitch1)+z1;
    %%%%%%%%%%%
    % pursuer %
    %%%%%%%%%%%
    losold=los;
    los=atan2(y1-y2,x1-x2);
    pitch=atan2(z1-z2,sqrt((x1-x2)^2+(y1-y2)^2));
    losrate=(los-losold);
    %[los*180/pi losrate*180/pi ]
    %los=-losrate*png+los
    dist=v2*dt;
    losmold=losm;
    losm=losm+losrate*png;
    losmrate=losm-losmold;
    %[losmrate/(maxlosm*dt)]
    if abs(losrate*png) > maxlosm*dt,
        losmrate=maxlosm*dt*sign(losmrate);
        losm=losmrate+losmold;
    end
    if abs(losmrate) > losmrate_max, 
        losmrate_max=abs(losmrate);
        losmrate_time=time;
        %[losmrate_time losmrate_max*180/pi/dt miss]
        %'oops'
        %break;
    end
    pngvalue=losmrate/losrate;
    [losrate*r2d/dt losmrate*r2d/dt miss dt pngvalue]
    %[time dt losmrate*180/pi/dt losmrate_max*180/pi/dt lomsrate_time]
    %if time>46.68, break;end
    x2=cos(losm)*dist*cos(pitch)+x2;
    y2=sin(losm)*dist*cos(pitch)+y2;
    z2=dist*sin(pitch)+z2;
    x2e=7000*cos(pitch)*cos(losm)+x2;
    y2e=7000*cos(pitch)*sin(losm)+y2;
    z2e=7000*sin(pitch)+z2;
    % miss
    %[time dt miss los]
    miss=sqrt((x1-x2)^2+(y1-y2)^2+(z1-z2)^2);
    ratio=miss/(v2*dt);
    if ratio < ratio_min, ratio_min=ratio;end
    %[ dt miss/(v2*dt) ratio_min miss]
    if miss/(v2*dt)>10 && miss/(v2*dt)<15,
        dt=0.01;
        %pause(0.1);
    end
    if miss < 1000,
        dt=0.01;
        %pause(0.001);
    end
    if miss < 500, dt=0.01;end
    if miss < intercept, break; end
    % plotting
    if use_plot == 0 % && mod(time,0.5)
        missa(i)=miss;
        x1a(i)=x1;
        y1a(i)=y1;
        z1a(i)=z1;
        x2a(i)=x2;
        y2a(i)=y2;
        z2a(i)=z2;
        timea(i)=time;
    end
    if use_plot == 1
        figure(10);
        %plot3(x1, y1, z1,'-o',x2,y2,z2,'x',x1,0,z1,'x');
        plot3(x1, y1, z1,'-o',x2,y2,z2,'x');
        % extended line
        %line([x1 x1e],[y1 y1e],[z1 z1e],'Color','r');
        %line([x2 x2e],[y2 y2e],[z2 z2e],'Color','m');
        % los line
        %line([x1 x2],[y1 y2],[z1 z2],'Color','c');
        if use_axis==1,axis([-50000 60000 0 60000 0 16000]);end
        xlabel('x');
        ylabel('y');
        zlabel('z');
        view([vx vy vz]);
        %axes('CameraPosition',[0 0 1]);
        grid on;
        hold on;
        title('Recording movie...')
    end
    % Get every frame with 'getframe' and load the appropriate       % matrix.
    if use_frame==1,
        frames(:, i) = getframe;
    end
    if use_avi==1,
        A=frames(:,i);
        aviobj = addframe(aviobj,A);
    end
    time=time+dt;
end
if use_plot == 1
    hold off
end
if use_avi==1,aviobj = close(aviobj);end

if use_plot == 0
    plot3(x1a,y1a,z1a,'-b',x2a,y2a,z2a,'-r');
    grid on;
    if use_axis==1,axis([-50000 60000 0 60000 0 16000]);end
    xlabel('x');
    ylabel('y');
    zlabel('z');
    view([vx vy vz]);
    %axes('CameraPosition',[0 0 1]);
    grid on;
    %figure(2);
    %plot(timea,missa);
end

%'time miss'
%[time miss]
sprintf('Time=%f Miss=%f xyz=%f,%f,%f',time,miss,x1,y1,z1)
% Save the matrix so that this movie can be loaded later
%save frames

