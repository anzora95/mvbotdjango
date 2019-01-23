// Setup the popup bubble
$(function(){
	$('.popupBubble').each(function(){
		// Options
		var distance = 10;
		var time = 100;
		var hideDelay = 500;
		
		var hideDelayTimer = null;
		
		// Tracker
		var beingShown = false;
		var shown = false;
		
		var trigger = $('.trigger', this);
		var popup = $('.popup', this).css('opacity',0);
		
		// Set the mouseover and mouseout on both element
		$([trigger.get(0), popup.get(0)]).mouseover(function(){
			// Stops the hide event if we move from the trigger to the popup element
			if(hideDelayTimer) clearTimeout(hideDelayTimer);
			
			// don't trigger the animation again if we're being shown, or already visible
			if(beingShown || shown) return;
			else{
				beingShown = true;
				
				// reset position of popup box
				popup.css({
					top:-75,
					left:-33,
					display:'block' // brings the popup back into view
				})				
				// (We're using chaining on the popup) now animate it's opacity and position
				.animate({
					top: '-=' + distance + 'px',
					opacity:1
				},time,'swing',function(){
					// once the animation is complete, set the tracker variables
					beingShown = false;
					shown = true;
				});
			}
		}).mouseout(function(){
			// reset the timer if we get fired again - avoids double animations
			if(hideDelayTimer)clearTimeout(hideDelayTimer);
			// Store the timer so that it can be cleared in the mouseover if required
			hideDelayTimer = setTimeout(function(){
				hideDelayTimer = null;
				popup.animate({
					top: '-=' + distance + 'px',
					opacity: 0
				}, time, 'swing', function(){
					// once the animate is complete, set the tracker variables
					shown = false;
					// hide the popup entirelet after the effect (opacity alone doesn't do the job)
					popup.css('display','none');
				});
			}, hideDelay);
		});
		
	});
});