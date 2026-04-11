using Microsoft.EntityFrameworkCore;
using FutebolApi;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddDbContext<AppDbContext>(options => options.UseSqlite("Data Source=futebol.db"));

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

//GET

app.MapGet("/", async (AppDbContext db) =>
{
    var times = await db.Times.ToListAsync();
    return Results.Ok(times);
    //return db.Times.ToListAsync();
});

app.MapGet("/times", async (AppDbContext db) =>
{
    var times = await db.Times.ToListAsync();
    return Results.Ok(times);
    //return db.Times.ToListAsync();
});

app.MapGet("/times/{id}", async (AppDbContext db, int id) =>
{
    var time = await db.Times.FindAsync(id);
    return time is not null ? Results.Ok(time) : Results.NotFound("Time não encontrado.");
});

//POST

app.MapPost("/times/new", async (AppDbContext db, Time time) =>
{
    db.Times.Add(time);
    await db.SaveChangesAsync();
    return Results.Created($"Time {time.Nome}, adicionado com sucesso!", time);
});

//PUT

app.MapPut("/times/{id}", async (int id, AppDbContext db, Time timeAtualizado) =>
{
    var time = await db.Times.FindAsync(id);
    if (time is null) return Results.NotFound("Time não encontrado.");

    time.Nome = timeAtualizado.Nome;
    time.Cidade = timeAtualizado.Cidade;
    time.TitulosBrasileiros = timeAtualizado.TitulosBrasileiros;
    time.TitulosMundiais = timeAtualizado.TitulosMundiais;

    await db.SaveChangesAsync();
    return Results.Ok(time);
});

app.MapDelete("/times/{id}", async (int id, AppDbContext db) =>
{
    var time = await db.Times.FindAsync(id);
    if (time is null) return Results.NotFound("Time não encontrado.");

    db.Times.Remove(time);
    await db.SaveChangesAsync();
    return Results.NoContent();
});

app.Run();
