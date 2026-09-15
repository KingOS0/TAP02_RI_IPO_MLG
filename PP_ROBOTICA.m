clear all
close all
clc

syms q1 q2 q3 q4 q5 q6 real

% Configuracion HOME en la convencion DH
offset = deg2rad([0 -90 180 180 180 90]);

% Tabla DH ORIGINAL
DH = [
      0,  deg2rad(0),      450,   q1;
    150,  deg2rad(-90),      0,   q2;
    600,  deg2rad(180),      0,   q3;
   -200,  deg2rad(90),    -640,   q4;
      0,  deg2rad(90),       0,   q5;
      0,  deg2rad(90),    -100,   q6;
      0,  deg2rad(0),        0,   0
];

T01 = T_DH(DH(1,1),DH(1,2),DH(1,3),DH(1,4));
T12 = T_DH(DH(2,1),DH(2,2),DH(2,3),DH(2,4));
T23 = T_DH(DH(3,1),DH(3,2),DH(3,3),DH(3,4));
T34 = T_DH(DH(4,1),DH(4,2),DH(4,3),DH(4,4));
T45 = T_DH(DH(5,1),DH(5,2),DH(5,3),DH(5,4));
T56 = T_DH(DH(6,1),DH(6,2),DH(6,3),DH(6,4));
T67 = T_DH(DH(7,1),DH(7,2),DH(7,3),DH(7,4));

T02 = simplify(T01*T12);
T03 = simplify(T02*T23);
T04 = simplify(T03*T34);
T05 = simplify(T04*T45);
T06 = simplify(T05*T56);
T07 = simplify(T06*T67);

O1 = T01(1:3,4);
O2 = T02(1:3,4);
O3 = T03(1:3,4);
O4 = T04(1:3,4);
O5 = T05(1:3,4);
O6 = T06(1:3,4);
O7 = T07(1:3,4);

z1 = T01(1:3,3);
z2 = T02(1:3,3);
z3 = T03(1:3,3);
z4 = T04(1:3,3);
z5 = T05(1:3,3);
z6 = T06(1:3,3);

Jv1 = cross(z1,O7-O1);
Jv2 = cross(z2,O7-O2);
Jv3 = cross(z3,O7-O3);
Jv4 = cross(z4,O7-O4);
Jv5 = cross(z5,O7-O5);
Jv6 = cross(z6,O7-O6);

% Pasamos la parte lineal de mm a m
Jv = simplify([Jv1 Jv2 Jv3 Jv4 Jv5 Jv6])/1000;

Jw = simplify([z1 z2 z3 z4 z5 z6]);

J = simplify([Jv;Jw]);

% PREPICK
q_prepick_moveit = [-0.5417750759524051 0.46047271225080777 0.21579062050232245 3.161468027539435 1.3585186541827539 -2.604341244084763];
q_prepick = q_prepick_moveit + offset;
J_prepick = double(subs(J,[q1 q2 q3 q4 q5 q6],q_prepick));

% PICK
q_pick_moveit = [-0.7752647813785839 1.1105386978136833 0.35293130240955367 3.177130932257688 0.8401946457796163 -2.390328130504908];
q_pick = q_pick_moveit + offset;
J_pick = double(subs(J,[q1 q2 q3 q4 q5 q6],q_pick));

% PRE_PLACE
q_preplace_moveit = [0.459276904895351 0.4012087905023365 0.4160061343874975 -3.0560897185874842 1.3279077240081203 2.6776838930620532];
q_preplace = q_preplace_moveit + offset;
J_preplace = double(subs(J,[q1 q2 q3 q4 q5 q6],q_preplace));

% PLACE
q_place_moveit = [0.7806358636969741 1.1995311919885967 0.6899406407535894 3.111631027448473 1.088190588062431 -2.9764161652134185];
q_place = q_place_moveit + offset;
J_place = double(subs(J,[q1 q2 q3 q4 q5 q6],q_place));

disp('Jacobiano en PREPICK:')
disp(J_prepick)

disp('Jacobiano en PICK:')
disp(J_pick)

disp('Jacobiano en PRE_PLACE:')
disp(J_preplace)

disp('Jacobiano en PLACE:')
disp(J_place)
%% Verificacion de velocidad 4B

%% Verificacion de velocidad 4B

q_4B_moveit = [-0.7199376875897102 0.8686946877686252 0.17984190382491727 3.173303046230387 0.910759814245635 -2.4414602027024577];

q_4B = q_4B_moveit + offset;

J_4B = double(subs(J,[q1 q2 q3 q4 q5 q6],q_4B));

prepick = [0.927 -0.560 0.927];
pick = [0.918 -0.903 0.322];

direccion_4B = (pick-prepick)/norm(pick-prepick);

v_perfil_4B = 0.200;

xdot_deseada_4B = [v_perfil_4B*direccion_4B 0 0 0]';

qdot_4B = pinv(J_4B)*xdot_deseada_4B;

xdot_verificada_4B = J_4B*qdot_4B;

v_lineal_4B = norm(xdot_verificada_4B(1:3));

disp('Velocidad cartesiana deseada 4B:')
disp(xdot_deseada_4B)

disp('Velocidad cartesiana verificada con J*qdot:')
disp(xdot_verificada_4B)

disp('Magnitud velocidad lineal 4B [m/s]:')
disp(v_lineal_4B)
%% Verificacion de velocidad 4D

q_4D_moveit = [0.5721032073363873 0.5519106812644714 0.31099301053994755 -3.162617450084051 1.3618731440550516 2.574179696617313];

q_4D = q_4D_moveit + offset;

J_4D = double(subs(J,[q1 q2 q3 q4 q5 q6],q_4D));

preplace = [0.942 0.457 1.116];
place = [0.966 0.961 0.430];

direccion_4D = (place-preplace)/norm(place-preplace);

v_perfil_4D = 0.100;

xdot_deseada_4D = [v_perfil_4D*direccion_4D 0 0 0]';

qdot_4D = pinv(J_4D)*xdot_deseada_4D;

xdot_verificada_4D = J_4D*qdot_4D;

v_lineal_4D = norm(xdot_verificada_4D(1:3));

disp('Velocidad cartesiana deseada 4D:')
disp(xdot_deseada_4D)

disp('Velocidad cartesiana verificada con J*qdot:')
disp(xdot_verificada_4D)

disp('Magnitud velocidad lineal 4D [m/s]:')
disp(v_lineal_4D)


function T_ij = T_DH(a_ij,alpha_ij,s_i,theta_i)



T_ij = [cos(theta_i),-sin(theta_i),0,a_ij;
        cos(alpha_ij)*sin(theta_i),cos(alpha_ij)*cos(theta_i),-sin(alpha_ij),-s_i*sin(alpha_ij);
        sin(alpha_ij)*sin(theta_i),sin(alpha_ij)*cos(theta_i),cos(alpha_ij),s_i*cos(alpha_ij);
        0,0,0,1];

end