if PlotType ~= 4
  caxis([0.8 1.2])
  axis([-2.5 2.5 -2.5 2.5])
  axis square
end

if PlotType==4
  axis([0 2.5 0 2.1])
  [rad1d,tref] = readamrdata(1,Frame,'./1drad/');
  if isempty(rad1d)
    disp('Run xclaw in rad1d directory to make reference solution')
    return
  end;
  if (abs(tref-t) > 1e-8)
    error('times are not compatible');
  end;
  hold on;
  [qref,xref,p] = plotframe1ez(rad1d,mq,'b-');
  set(p,'LineWidth',2);

  h2d = getlegendinfo;
  str1 = sprintf('2d solution (mx = %d)',mx);
  str2 = sprintf('1d solution (mx = %d)',length(xref));
  legend([h2d,p],str1,str2);
  hold off;

  % (xcenter,ycenter) and (x0,y0) are in memory.
  [xcm,ycm] = meshgrid(xcenter,ycenter);
  rcm = sqrt((xcm - x0).^2 + (ycm - y0).^2);

  % Use (xref,qref) returned from
  qcm = interp1(xref,qref,rcm,'*cubic');
  ecm = abs(qcm-qmesh);

  figure(2);
  pc = pcolor(xcm,ycm,ecm);
  set(pc,'EdgeColor','none');
  caxis([0 0.05]);
  axis square;
  colorbar;
  title(sprintf('Maximum error : %12.4e',max(max(ecm))));

  figure(1);


end

clear afterframe;
